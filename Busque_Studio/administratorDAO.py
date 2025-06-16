import tkinter as tk
from tkinter import messagebox
import mysql.connector


class AdministradorDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, administrador):
        sql= "INSERT INTO administrador (id_perfil, nome, email, login, senha) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (administrador.id_perfil, administrador.nome, administrador.email, administrador.login, administrador.senha))
        self.cursor.commit()

    def listar(self):
        self.cursor.execute ("SELECT * FROM administrador")
        return self.cursor.fechall()
    
    def atualizar(self, administrador):
        sql = "UPDATE SET id_perfil = %s, nome = %s, email = %s, login = %s, senha = %s WHERE id_administrador = %s"
        self.cursor.execute(sql, (administrador.id_perfil, administrador.nome, administrador.email, administrador.login, administrador.senha))
        self.conexao.commit()

    def deletar(self,id_administrador):
        sql = "DELETE FROM administrador WHERE id_administrador = %s"
        self.cursor.execute(sql,(id_administrador,))
        self.cursor.commit()


