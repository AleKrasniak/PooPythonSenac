import tkinter as tk
from tkinter import messagebox
import mysql.connector

class UsuarioDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sistema"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, usuario):
        sql = "INSERT INTO usuarios (nome, email) VALUES (%s, %s)"
        self.cursor.execute(sql, (usuario.nome, usuario.email))
        self.conexao.commit

    def listar(self):
        self.cursor.execute("SELECT * FROM  usuarios")
        return self.cursor.fetchall()
    
    def atualizar(self, usuario):
        sql = "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s"
        self.cursor.execute(sql, (usuario.nome, usuario.email, usuario.id))
        self.conexao.commit()

    def deletar(self, id):
        sql = "DELETE FROM usuarios WHERE id = %s"
        self.cursor.execute(sql,(id,))
        self.conexao.commit()
