import tkinter as tk
from tkinter import messagebox
import mysql.connector


class AvalicaoDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, avaliacao):
        sql = "INSERT INTO avaliacao (id_cliente, id_estudio, nota, comentario, data_avaliacao) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql,(avaliacao.id_cliente, avaliacao.id_estudio, avaliacao.nota, avaliacao.comentario, avaliacao.data_avaliacao))
        self.cursor.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM avaliacao")
        return self.cursor.fetchall()

    def atualizar (self, avaliacao):
        sql = "UPDATE avaliacao SET id_cliente = %s, id_estudio = %s, nota = %s, comentario = %s, data_avaliacao = %s WHERE id_avaliacao =%s"
        self.cursor.execute(sql, (avaliacao.id_cliente, avaliacao.id_estudio, avaliacao.nota, avaliacao.comentario, avaliacao.data_avaliacao, avaliacao.id_avaliacao))
        self.conexao.commit()

    def deletar (self, id_avaliacao):
        sql = "DELETE FROM avaliacao WHERE id_avaliacao = %s"
        self.cursor.execute(sql,(id_avaliacao,))
        self.conexao.commit()



# def __init__(self, id_agendamento=None, id_cliente=None, id_estudio=None, nota=None, comentario="", data_avaliacao=None,):
#         self.id_avaliacao = id_avaliacao
#         self.id_cliente = id_cliente
#         self.id_estudio = id_estudio
#         self.nota = nota
#         self.comentario = comentario
#         self.data_avalicao = data_avaliacao or datetime.now()