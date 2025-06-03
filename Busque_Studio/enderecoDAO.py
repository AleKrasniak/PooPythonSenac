import tkinter as tk
from tkinter import messagebox
import mysql.connector
import requests


class EnderecoDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.cursor()

    def criar(self, endereco):
        sql = "INSERT INTO endereco (rua, numero, bairro, cidade, complemento, uf, cep, data_cadastro, data_atualizacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (endereco.rua, endereco.numero, endereco.bairro, endereco.cidade, endereco.complemento, endereco.uf, endereco.cep, endereco.data_cadastro, endereco.data_atualizacao))
        self.conexao.commit()
    
    def listar(self):
        self.cursor.execute("SELECT * FROM endereco")
        return self.cursor.fetchall()
    
    def atualizar(self, endereco):
        sql = "UPDATE endereco SET rua = %s, numero = %s, bairro = %s, cidade = %s, complemento = %s, uf = %s, cep= %s, data_atualizacao = %s WHERE id_endereco = %s"
        self.cursor.execute(sql(endereco.rua, endereco.numero, endereco.bairro, endereco.cidade, endereco.complemento, endereco.uf, endereco.cep, endereco.data_atualizacao, endereco.id_endereco ))
        self.conexao.commit()

    def deletar(self, id_endereco):
        sql = "DELETE FROM endereco WHERE id_endereco = %s"
        self.cursor.execute(sql, (id_endereco,))
        self.conexao.commit()

        # Buscar todos os estados (UFs) pelo IBGE
    def listar_estados(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            estados = [{'id': est['id'], 'sigla': est['sigla'], 'nome': est['nome']} for est in resposta.json()]
            estados.sort(key=lambda x: x['nome'])
            return estados
        else:
            raise Exception("Erro ao buscar estados do IBGE")

    # Buscar cidades de um estado (UF) pelo IBGE
    def listar_cidades_por_uf(self, uf):
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            cidades = [cidade['nome'] for cidade in resposta.json()]
            cidades.sort()
            return cidades
        else:
            raise Exception(f"Erro ao buscar cidades para o estado {uf}")

    # Fechar conexão com o banco
    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()

        # self.id_endereco = id_endereco
        # self.rua = rua
        # self.numero = numero
        # self.bairro = bairro
        # self.cidade = cidade
        # self.complemento = complemento
        # self.uf = uf 
        # self.cep = cep
        # self.data_cadastro = data_cadastro or datetime.now()
        # self.data_atualizacao = data_atualizacao or datetime.now()