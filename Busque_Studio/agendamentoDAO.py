import tkinter as tk
from tkinter import messagebox
import mysql.connector

class agendamentoDAO:
    def __init__(self):
        self.conexao = mysql.connector.conect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
    )
        self.cursor = self.conexao.cursor()

    def criar(self, agendamento):
        sql = "INSERT INTO agendamento (id_cliente, id_estudio, id_profissional, data_hora, valor, status) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql,(agendamento.id_cliente, agendamento.id_estudio, agendamento.id_profissional, agendamento.data_hora, agendamento.valor, agendamento.status))
        self.conexao.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM agendamento")
        return self.cursor.fetchall()

    def atualizar(self, agendamento):
        sql = "UPDATE agendamento SET id_cliente = %s, id_estudio = %s, id_profissional = %s, data_hora = %s, valor = %s, status = %s WHERE id_agendamento = %s"
        self.cursor.execute(sql, (agendamento.id_cliente, agendamento.id_estudio, agendamento.id_profissional, agendamento.data_hora, agendamento.valor, agendamento.status, agendamento.id_agendamento))
        self.conexao.commit()

    def deletar(self, id_agendamento):
        sql = "DELETE FROM agendamento WHERE id_agendamento = %s"
        self.cursor.execute(sql,(id_agendamento))
        self.conexao.commit()



        # def __init__(self, id_agendamento=None, id_cliente=None, id_estudio=None, id_profissional=None, data_hora=None, valor=None, status="Agendado"):
        # self.id_agendamento = id_agendamento
        # self.id_cliente = id_cliente
        # self.id_estudio = id_estudio
        # self.id_profissional = id_profissional
        # self.data_hora = data_hora or datetime.now()
        # self.valor = valor
        # self.status = status