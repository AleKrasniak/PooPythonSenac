import mysql.connector
from datetime import datetime
from mysql.connector import Error, pooling
from typing import Dict, List, Optional
import time

class EstudioDAO:
    def __init__(self):
        """Inicializa o DAO com pool de conexões"""
        self.connection_pool = self._create_connection_pool()
        self.max_retries = 3
        self.retry_delay = 1  # segundos

    def _create_connection_pool(self):
        """Cria um pool de conexões com o MySQL"""
        try:
            return pooling.MySQLConnectionPool(
                pool_name="estudio_pool",
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
                
                if err.errno == 2006:  # MySQL server has gone away
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

    def criar_estudio(self, estudio_data: Dict) -> int:
        """Cria um novo estúdio no banco de dados"""
        try:
            # Primeiro insere o endereço
            endereco_query = """INSERT INTO endereco 
                              (rua, numero, bairro, cidade, complemento, uf, cep, data_cadastro, data_atualizacao) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            endereco_params = (
                estudio_data.get('rua', 'Não informado'),
                estudio_data.get('numero', 0),
                estudio_data.get('bairro', 'Não informado'),
                estudio_data.get('cidade', ''),
                estudio_data.get('complemento', 'Não informado'),
                estudio_data.get('uf', ''),
                estudio_data.get('cep', ''),
                datetime.now(),
                datetime.now()
            )
            
            cursor = self._execute_query(endereco_query, endereco_params)
            id_endereco = cursor.lastrowid
            
            # Depois insere o estudio
            estudio_query = """INSERT INTO estudio 
                             (id_perfil, id_endereco, nome, cnpj, descricao, login, senha, tipo, foto_perfil) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            estudio_params = (
                estudio_data.get('id_perfil'),
                id_endereco,
                estudio_data.get('nome'),
                estudio_data.get('cnpj'),
                estudio_data.get('descricao'),
                estudio_data.get('login'),
                estudio_data.get('senha'),
                estudio_data.get('tipo'),
                estudio_data.get('foto_perfil', None)
            )
            
            cursor = self._execute_query(estudio_query, estudio_params)
            return cursor.lastrowid
            
        except Exception as e:
            raise Exception(f"Erro ao criar estúdio: {str(e)}")

    def buscar_por_login(self, login: str) -> Optional[Dict]:
        """Busca um estúdio pelo login"""
        try:
            query = """SELECT e.*, en.rua, en.numero, en.bairro, en.cidade, 
                      en.complemento, en.uf, en.cep, en.id_endereco
                      FROM estudio e
                      JOIN endereco en ON e.id_endereco = en.id_endereco
                      WHERE e.login = %s"""
            result = self._execute_query(query, (login,), fetch=True)
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Erro ao buscar por login: {str(e)}")

    def buscar_por_id(self, id_estudio: int) -> Optional[Dict]:
        """Busca um estúdio pelo ID"""
        try:
            query = """SELECT e.*, en.rua, en.numero, en.bairro, en.cidade, 
                      en.complemento, en.uf, en.cep, en.id_endereco
                      FROM estudio e
                      JOIN endereco en ON e.id_endereco = en.id_endereco
                      WHERE e.id_estudio = %s"""
            result = self._execute_query(query, (id_estudio,), fetch=True)
            return result[0] if result else None
        except Exception as e:
            raise Exception(f"Erro ao buscar estúdio por ID: {str(e)}")

    def atualizar_estudio(self, estudio_data: Dict) -> bool:
        """Atualiza os dados de um estúdio"""
        try:
            # Atualiza endereço
            endereco_query = """UPDATE endereco SET
                              rua = %s, numero = %s, bairro = %s,
                              cidade = %s, complemento = %s,
                              uf = %s, cep = %s, data_atualizacao = %s
                              WHERE id_endereco = %s"""
            endereco_params = (
                estudio_data.get('rua'),
                estudio_data.get('numero'),
                estudio_data.get('bairro'),
                estudio_data.get('cidade'),
                estudio_data.get('complemento'),
                estudio_data.get('uf'),
                estudio_data.get('cep'),
                datetime.now(),
                estudio_data.get('id_endereco')
            )
            self._execute_query(endereco_query, endereco_params)
            
            # Atualiza estúdio
            estudio_query = """UPDATE estudio SET
                             nome = %s, cnpj = %s, descricao = %s,
                             login = %s, senha = %s, tipo = %s,
                             foto_perfil = %s
                             WHERE id_estudio = %s"""
            estudio_params = (
                estudio_data.get('nome'),
                estudio_data.get('cnpj'),
                estudio_data.get('descricao'),
                estudio_data.get('login'),
                estudio_data.get('senha'),
                estudio_data.get('tipo'),
                estudio_data.get('foto_perfil'),
                estudio_data.get('id_estudio')
            )
            self._execute_query(estudio_query, estudio_params)
            
            return True
        except Exception as e:
            raise Exception(f"Erro ao atualizar estúdio: {str(e)}")

    def deletar_estudio(self, id_estudio: int) -> bool:
        """Remove um estúdio do banco de dados"""
        try:
            # Primeiro obtém o ID do endereço
            query = "SELECT id_endereco FROM estudio WHERE id_estudio = %s"
            result = self._execute_query(query, (id_estudio,), fetch=True)
            
            if not result:
                raise Exception("Estúdio não encontrado")
                
            id_endereco = result[0]['id_endereco']
            
            # Deleta o estúdio
            self._execute_query("DELETE FROM estudio WHERE id_estudio = %s", (id_estudio,))
            
            # Deleta o endereço
            self._execute_query("DELETE FROM endereco WHERE id_endereco = %s", (id_endereco,))
            
            return True
        except Exception as e:
            raise Exception(f"Erro ao deletar estúdio: {str(e)}")

    def listar_estudios(self) -> List[Dict]:
        """Lista todos os estúdios cadastrados"""
        try:
            query = """SELECT e.*, en.rua, en.numero, en.bairro, en.cidade, en.uf
                      FROM estudio e
                      JOIN endereco en ON e.id_endereco = en.id_endereco
                      ORDER BY e.nome"""
            return self._execute_query(query, fetch=True)
        except Exception as e:
            raise Exception(f"Erro ao listar estúdios: {str(e)}")