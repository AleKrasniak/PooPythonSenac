import mysql.connector
from datetime import datetime
from mysql.connector import Error, pooling
from typing import Dict, List, Optional
import time

class AlvaraDAO:
    def __init__(self):
        """Inicializa o DAO com pool de conexões"""
        self.connection_pool = self._create_connection_pool()
        self.max_retries = 3
        self.retry_delay = 1

    def _create_connection_pool(self):
        """Cria um pool de conexões com o MySQL"""
        try:
            return pooling.MySQLConnectionPool(
                pool_name="alvara_pool",
                pool_size=5,
                host="localhost",
                user="root",
                password="",
                database="busquestudios2",
                autocommit=False
            )
        except Error as err:
            raise Exception(f"Erro ao criar pool de conexões: {err}")

    def _execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """Executa uma query com tratamento de erros e retry automático"""
        connection = None
        cursor = None
        
        for attempt in range(self.max_retries):
            try:
                connection = self.connection_pool.get_connection()
                cursor = connection.cursor(dictionary=True)
                
                cursor.execute(query, params or ())
                
                if fetch:
                    result = cursor.fetchall()
                    connection.commit()
                    return result
                else:
                    connection.commit()
                    return cursor
                    
            except Error as err:
                if connection:
                    connection.rollback()
                
                if err.errno == 2006:
                    if attempt == self.max_retries - 1:
                        raise Exception(f"Erro ao executar query após {self.max_retries} tentativas: {err}")
                    time.sleep(self.retry_delay)
                    continue
                raise Exception(f"Erro ao executar query: {err}")
            finally:
                if cursor:
                    cursor.close()
                if connection and connection.is_connected():
                    connection.close()

    def criar(self, alvara) -> int:
        """Cria um novo alvará no banco de dados"""
        try:
            query = """INSERT INTO alvara (id_estudio, numero_alvara, tipo_alvara, 
                      data_emissao, data_validade, status, descricao, documento_anexo) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (
                alvara.id_estudio, 
                alvara.numero_alvara, 
                alvara.tipo_alvara, 
                alvara.data_emissao, 
                alvara.data_validade, 
                alvara.status, 
                alvara.descricao, 
                alvara.documento_anexo
            )
            
            cursor = self._execute_query(query, params)
            return cursor.lastrowid
            
        except Exception as e:
            raise Exception(f"Erro ao criar alvará: {str(e)}")

    def listar(self) -> List[Dict]:
        """Lista todos os alvarás cadastrados"""
        try:
            query = "SELECT * FROM alvara ORDER BY data_emissao DESC"
            return self._execute_query(query, fetch=True)
        except Exception as e:
            raise Exception(f"Erro ao listar alvarás: {str(e)}")
    
    def buscar_por_id(self, id_alvara: int) -> Optional[Dict]:
        """Busca um alvará pelo ID"""
        try:
            query = "SELECT * FROM alvara WHERE id_alvara = %s"
            result = self._execute_query(query, (id_alvara,), fetch=True)
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Erro ao buscar alvará por ID: {str(e)}")
    
    def buscar_por_estudio(self, id_estudio: int) -> List[Dict]:
        """Busca todos os alvarás de um estúdio específico"""
        try:
            query = "SELECT * FROM alvara WHERE id_estudio = %s ORDER BY data_emissao DESC"
            return self._execute_query(query, (id_estudio,), fetch=True)
        except Exception as e:
            raise Exception(f"Erro ao buscar alvarás por estúdio: {str(e)}")
    
    def atualizar(self, alvara) -> bool:
        """Atualiza os dados de um alvará"""
        try:
            query = """UPDATE alvara SET id_estudio = %s, numero_alvara = %s, 
                      tipo_alvara = %s, data_emissao = %s, data_validade = %s, 
                      status = %s, descricao = %s, documento_anexo = %s 
                      WHERE id_alvara = %s"""
            params = (
                alvara.id_estudio, 
                alvara.numero_alvara, 
                alvara.tipo_alvara, 
                alvara.data_emissao, 
                alvara.data_validade, 
                alvara.status, 
                alvara.descricao, 
                alvara.documento_anexo,
                alvara.id_alvara
            )
            
            self._execute_query(query, params)
            return True
        except Exception as e:
            raise Exception(f"Erro ao atualizar alvará: {str(e)}")

    def deletar(self, id_alvara: int) -> bool:
        """Remove um alvará do banco de dados"""
        try:
            query = "DELETE FROM alvara WHERE id_alvara = %s"
            self._execute_query(query, (id_alvara,))
            return True
        except Exception as e:
            raise Exception(f"Erro ao deletar alvará: {str(e)}")