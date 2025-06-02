import tkinter as tk
from tkinter import messagebox
import mysql.connector



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