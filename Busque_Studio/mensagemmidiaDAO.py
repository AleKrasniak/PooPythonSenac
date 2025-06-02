import tkinter as tk
from tkinter import messagebox
import mysql.connector

class MensagemmidiaDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, mensagemmidia):
        sql = "INSERT INTO mensagemmidia (id_mensagem, url, tipo) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (mensagemmidia.id_mensagem, mensagemmidia.url, mensagemmidia.tipo))
        self.conexao.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM mensagemmidia")
        return self.cursor.fetchall()

    def atualizar(self, mensagemmidia):
        sql = "UPDATE mensagemmidia SET id_mensagem = %s, url = %s, tipo = %s WHERE id_mensagemmidia = %s"
        self.cursor.execute(sql, (mensagemmidia.id_mensagem, mensagemmidia.url, mensagemmidia.tipo, mensagemmidia.id_mensagem_midia))
        self.conexao.commit()

    def deletar(self, id_mensagem_midia):
        sql = "DELETE FROM mensagemmidia WHERE id_mensagem_midia = %s"
        self.cursor.execute(sql,(id_mensagem_midia))
        self.conexao.commit()

    



        #     def __init__(self, id_mensagem_midia=None, id_mensagem=None, url="", tipo=""):
        # self.id_mensagem_midia = id_mensagem_midia
        # self.id_mensagem = id_mensagem
        # self.url = url
        # self.tipo = tipo