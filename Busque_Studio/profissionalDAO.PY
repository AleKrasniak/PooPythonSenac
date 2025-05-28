import tkinter as tk
from tkinter import messagebox
import mysql.connector

class ProfissionalDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, profissional):
        sql = "INSERT INTO profissional (id_estudio, nome, cpf, especialidade) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (profissional.id_estudio, profissional.nome, profissional.cpf, profissional.especialidade))
        self.conexao.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM profissional")
        return self.cursor.fetchall()
    
    def atualizar(self, profissional):
        sql = "UPDATE chat SET id_estudio = %s, nome = %s, cpf = %s, especialidade= %s WHERE id_profissional = %s"
        self.cursor.execute(sql,(profissional.id_estudio, profissional.nome, profissional.cpf, profissional.especialidade, profissional.id_profissional))
        self.conexao.commit()

    def deletar(self, id_profissional):
        sql = "DELETE FROM profissional WHERE id_profissional = %s"
        self.cursor.execute(sql,(id_profissional))
        self.conexao.commit()


    # def __init__(self, id_profissional=None, id_estudio=None, nome="", cpf="", especialidade=""):
    #     self.id_profissional = id_profissional
    #     self.id_estudio = id_estudio
    #     self.nome = nome
    #     self.cpf = cpf
    #     self.especialidade= especialidade