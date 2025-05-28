import tkinter as tk 
from tkinter import messagebox
import mysql.connector
from perfil import Perfil

class perfilDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )

        self.cursor = self.conexao.cursor()

    def criar(self, perfil):
        sql = "INSERT INTO perfil (NOME, DESCRICAO) VALUES (%s, %s)"
        self.cursor.execute(sql,(perfil.DESCRICAO, perfil.DESCRICAO ))
        self.conexao.commit()


    def listar(self):
        self.cursor.execute("SELECT * FROM perfil")
        return self.cursor.fetchall()
    
    def atualizar(self, perfil):
        sql = "UPDATE perfil SET NOME = %s, DESCRICAO = %s WHERE id_perfil = %s"
        self.cursor.execute(sql, (perfil.NOME, perfil.DESCRICAO, perfil.ID_PERFIL))
        self.conexao.commit()

    def deletar(self, id_perfil):
        sql = "DELETE FROM perfil WHERE id_perfil = %s"
        self.cursor.execute(sql,(id_perfil,))  
        self.conexao.commit()


