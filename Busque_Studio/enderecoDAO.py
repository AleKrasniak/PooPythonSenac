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
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.connection.cursor(dictionary=True)
        self._verificar_conexao()  # <-- Verifica logo ao iniciar

    # --- FUNÇÃO ANTI-DESCONEXÃO ---
    def _verificar_conexao(self):
        """Versão turbo com mais tentativas e logs"""
        for tentativa in range(3):  # Tenta 3 vezes
            try:
                if not self.connection.is_connected():
                    print(f"⚠️ Tentando reconectar ({tentativa+1}/3)...")
                    self.connection.reconnect(attempts=3, delay=1)
                    self.cursor = self.connection.cursor(dictionary=True)
                return  # Conexão OK!
            except Error as err:
                if tentativa == 2:  # Última tentativa
                    raise DatabaseConnectionError(f"Falha após 3 tentativas: {err}")
                time.sleep(1)

    def criar(self, endereco):
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

    def listar(self):
        self.cursor.execute("SELECT * FROM endereco")
        return self.cursor.fetchall()

    def atualizar(self, endereco):
        sql = "UPDATE endereco SET rua = %s, numero = %s, bairro = %s, cidade = %s, complemento = %s, uf = %s, cep = %s, data_atualizacao = %s WHERE id_endereco = %s"
        self.cursor.execute(sql, (
            endereco.rua, endereco.numero, endereco.bairro, endereco.cidade,
            endereco.complemento, endereco.uf, endereco.cep,
            endereco.data_atualizacao, endereco.id_endereco
        ))
        self.conexao.commit()

    def deletar(self, id_endereco):
        sql = "DELETE FROM endereco WHERE id_endereco = %s"
        self.cursor.execute(sql, (id_endereco,))
        self.conexao.commit()

    def listar_estados(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            estados = [{'id': est['id'], 'sigla': est['sigla'], 'nome': est['nome']} for est in resposta.json()]
            estados.sort(key=lambda x: x['nome'])
            return estados
        else:
            raise Exception("Erro ao buscar estados do IBGE")

    def listar_cidades_por_uf(self, uf):
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            cidades = [cidade['nome'] for cidade in resposta.json()]
            cidades.sort()
            return cidades
        else:
            raise Exception(f"Erro ao buscar cidades para o estado {uf}")

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()
