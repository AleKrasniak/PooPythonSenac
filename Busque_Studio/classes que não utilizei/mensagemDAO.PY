import tkinter as tk
from tkinter import messagebox
import mysql.connector

class MensagemDAO:
    def __init__(self):
        self.conexao.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, mensagem):
        sql = "INSERT INTO mensagem (id _chat, texto, data_envio, remetente_tipo, status) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (mensagem.id _chat, mensagem.texto, mensagem.data_envio, mensagem.remetente_tipo, mensagem.status))
        self.conexao.commit

    def listar(self):
        self.cursor.execute("SELECT * FROM mensagem")
        return self.cursor.fetchall()

    def atualizar(self, mensagem):
        sql = "UPDATE mensagem SET id _chat = %s, texto = %s, data_envio = %s, remetente_tipo = %s, status = %s WHERE id_mensagem = %s"
        self.cursor.execute(sql, (mensagem.id _chat, mensagem.texto, mensagem.data_envio, mensagem.remetente_tipo, mensagem.status, mensagem.id_mensagem))
        self.conexao.commit()

    def deletar(self, id_mensagem):
        sql = "DELETE FROM mensagem WHERE id_mensagem - %s"
        self.cursor.execute(sql,(id_mensagem))
        self.conexao.commit()


    # def __init__(self, id_mensagem=None, id_chat=None, texto="", data_envio=None, remetente_tipo="", status="Enviada",):
    #     self.id_mensagem = id_mensagem
    #     self.id_chat = id_chat
    #     self.texto = texto
    #     self.data_envio = data_envio
    #     self.remetente_tipo = remetente_tipo
    #     self.status = status