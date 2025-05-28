import tkinter as tk
from tkinter import messagebox
import mysql.connector

class PermissaoDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
             host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()
    def criar(self, permissao):
        sql = "INSERT INTO permissao (nome, descricao) VALUES (%s, %d)"
        self.cursor.execute(sql, (permissao.nome, permissao.descricao))
        self.conexao.commit

    def listar(self):
        self.cursor.execute("SELECT * FROM permissao")
        return self.cursor.fetchall()
    
    def atualizar(self, permissao):
        sql = "UPDATE permissao SET nome = %s, descricao = %s WHERE id_permissao = %s "
        self.cursor.execute(sql, (permissao.nome, permissao.descricao, permissao.id_permissao))
        self.conexao.commit()

    def deletar (self, id_permissao):
        sql = "DELE FROM permissao WHERE id = %s"
        self.cursor.execute(sql, (id_permissao,))
        self.conexao.commit()