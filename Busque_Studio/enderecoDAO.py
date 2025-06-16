import tkinter as tk
from tkinter import messagebox
import mysql.connector
import requests
from mysql.connector import Error
import time 

class DatabaseConnectionError(Exception):
    """Exceção para erros de conexão com o banco"""
    pass

class EnderecoDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor(dictionary=True)
        self._verificar_conexao()

    def _verificar_conexao(self):
        """Versão turbo com mais tentativas e logs"""
        for tentativa in range(3):
            try:
                if not self.conexao.is_connected():
                    print(f"⚠️ Tentando reconectar ({tentativa+1}/3)...")
                    self.conexao.reconnect(attempts=3, delay=1)
                    self.cursor = self.conexao.cursor(dictionary=True)
                return
            except Error as err:
                if tentativa == 2:
                    raise DatabaseConnectionError(f"Falha após 3 tentativas: {err}")
                time.sleep(1)

    def criar(self, endereco):
        """Cria um novo endereço no banco"""
        self._verificar_conexao()
        sql = """INSERT INTO endereco 
                (rua, numero, bairro, cidade, complemento, uf, cep, data_cadastro, data_atualizacao) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql, (
            endereco.rua, endereco.numero, endereco.bairro, endereco.cidade,
            endereco.complemento, endereco.uf, endereco.cep,
            endereco.data_cadastro, endereco.data_atualizacao
        ))
        self.conexao.commit()
        return self.cursor.lastrowid 

    def buscar_por_id(self, id_endereco):
        """Busca um endereço específico pelo ID"""
        self._verificar_conexao()
        try:
            sql = "SELECT * FROM endereco WHERE id_endereco = %s"
            self.cursor.execute(sql, (id_endereco,))
            resultado = self.cursor.fetchone()
            return resultado
        except Exception as e:
            print(f"Erro ao buscar endereço por ID {id_endereco}: {e}")
            return None

    def listar(self):
        """Lista todos os endereços"""
        self._verificar_conexao()
        self.cursor.execute("SELECT * FROM endereco")
        return self.cursor.fetchall()

    def atualizar(self, endereco):
        """Atualiza um endereço existente"""
        self._verificar_conexao()
        sql = """UPDATE endereco SET 
                rua = %s, numero = %s, bairro = %s, cidade = %s, 
                complemento = %s, uf = %s, cep = %s, data_atualizacao = %s 
                WHERE id_endereco = %s"""
        self.cursor.execute(sql, (
            endereco.rua, endereco.numero, endereco.bairro, endereco.cidade,
            endereco.complemento, endereco.uf, endereco.cep,
            endereco.data_atualizacao, endereco.id_endereco
        ))
        self.conexao.commit()

    def deletar(self, id_endereco):
        """Deleta um endereço"""
        self._verificar_conexao()
        sql = "DELETE FROM endereco WHERE id_endereco = %s"
        self.cursor.execute(sql, (id_endereco,))
        self.conexao.commit()

    def listar_estados(self):
        """Busca lista de estados do IBGE"""
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            estados = [{'id': est['id'], 'sigla': est['sigla'], 'nome': est['nome']} for est in resposta.json()]
            estados.sort(key=lambda x: x['nome'])
            return estados
        else:
            raise Exception("Erro ao buscar estados do IBGE")

    def listar_cidades_por_uf(self, uf):
        """Busca cidades por UF do IBGE"""
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            cidades = [cidade['nome'] for cidade in resposta.json()]
            cidades.sort()
            return cidades
        else:
            raise Exception(f"Erro ao buscar cidades para o estado {uf}")

    def buscar_cidades_por_nome(self, nome_cidade):
        """Busca endereços por nome da cidade"""
        self._verificar_conexao()
        try:
            sql = "SELECT * FROM endereco WHERE cidade LIKE %s"
            self.cursor.execute(sql, (f"%{nome_cidade}%",))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar endereços por cidade {nome_cidade}: {e}")
            return []

    def fechar_conexao(self):
        """Fecha a conexão com o banco"""
        if self.cursor:
            self.cursor.close()
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()