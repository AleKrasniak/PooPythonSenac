import tkinter as tk
from tkinter import messagebox
import mysql.connector
from perfil import Perfil
from permissao import Permissao

class Perfil_PermissaoDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, perfil_permissao):
        sql = "INSERT INTO perfil_permissao (id_perfil, id_permissao) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (perfil_permissao.id_perfil, perfil_permissao.id_permissao))
        self.conexao.commit

    def listar (self):
        self.cursor.execute("SELECT * FROM perfil_permissao")
        return self.cursor.fetchall()
    
    def atualizar (self, perfil_permissao):
        sql = "UPDATE perfil_permissao SET id_perfil = %s, id_permissao = %s WHERE id_perfil_permissao = %s"
        self.cursor.execute(sql, (perfil_permissao.id_perfil, perfil_permissao.id_permissao, perfil_permissao.id_perfil_permissao))
        self.conexao.commit()

    def deletar(self, id_perfil_permissao): 
        sql = "DELETE FROM perfil_permissao WHERE id_perfil_permissao =%s"
        self.cursor.execute(sql,(id_perfil_permissao,))
        self.conexao.commit




# CREATE TABLE PERFIL_PERMISSAO(
# ID_PERFIL INT NOT NULL,
# ID_PERMISSAO INT NOT NULL,
# PRIMARY KEY (ID_PERFIL, ID_PERMISSAO),
# FOREIGN KEY (ID_PERFIL) REFERENCES PERFIL(ID_PERFIL)
# ON UPDATE CASCADE
# ON DELETE CASCADE,
# FOREIGN KEY (ID_PERMISSAO) REFERENCES PERMISSAO(ID_PERMISSAO)
# ON UPDATE CASCADE
# ON DELETE CASCADE