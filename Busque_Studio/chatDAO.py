import tkinter as tk
from tkinter import messagebox
import mysql.connector

class ChatDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, chat):
        sql = "INSERT INTO chat (data_inicio, id_cliente, id_estudio) VALUES (%s, %s, %s)"
        self.cursor.execute(sql,(chat.data_inicio, chat.id_cliente, chat.id_estudio))
        self.conexao.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM chat")
        return self.cursor.fetchall()
    
    def atualizar(self, chat):
        sql= "UPDATE chat SET data_inicio = %s, id_cliente = %s, id_estudio = %s WHERE id_chat = %s"
        self.cursor.execute(sql, (chat.data_inicio, chat.id_cliente, chat.id_estudio, chat.id_chat))
        self.conexao.commit()

    def deletar (self, id_chat):
        sql = "DELETE FROM chat WHERE id_chat = %s"
        self.cursor.execute(sql,(id_chat,))
        self.conexao.commit()






# import tkinter as tk
# from tkinter import messagebox
# import mysql.connector
# from cliente import Cliente
# from estudio import Estudio
# from datetime import datetime 

# class Chat:
#     def __init__(self, id_chat=None, data_inicio=None, id_cliente=None, id_estudio=None):
#         self.id_chat = id_chat
#         self.data_inicio = data_inicio
#         self.id_cliente = id_cliente
#         self.id_estudio = id_estudio