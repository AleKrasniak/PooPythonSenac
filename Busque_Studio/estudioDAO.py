import tkinter as tk
from tkinter import messagebox
import mysql.connector


class EstudioDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

        def criar(self, estudio):
            sql= "INSERT INTO estudio (id_perfil, id_endereco, nome, cnpj, descricao, login, senha, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql, (estudio.id_perfil, estudio.id_endereco, estudio.nome, estudio.cnpj, estudio.descricao, estudio.login, estudio.senha, estudio.tipo ))
            self.conexao.commit()
        
        def listar(self):
            self.cursor.execute("SELECT * FROM estudio")
            return self.cursor.fetchall()
        
        def atualizar(self, estudio):
            sql = "UPDATE estudio SET id_perfil = %s, id_endereco = %s, nome = %s, cnpj = %s, descricao = %s, login = %s, senha = %s, tipo = %s WHERE id_cliente = %s"
            self.cursor.execute(sql,(estudio.id_perfil, estudio.id_endereco, estudio.nome, estudio.cnpj, estudio.descricao, estudio.login, estudio.senha, estudio.tipo))
            self.conexao.commit()

        def deletar(self, id_estudio):
            sql = "DELETE FROM cliente WHERE id_estudio = %s"
            self.cursor.execute(sql,(id_estudio,))
            self.conexao.commit()




    # def __init__(self, id_estudio=None, id_perfil=None, id_endereco=None, nome="", cnpj="", descricao="", login="", senha="", tipo="" ):
    #     self.id_estudio = id_estudio
    #     self.id_perfil = id_perfil
    #     self.id_endereco = id_endereco
    #     self.nome = nome 
    #     self.cnpj = cnpj
    #     self.desricao = descricao
    #     self.login = login
    #     self.senha = senha
    #     self.tipo = tipo