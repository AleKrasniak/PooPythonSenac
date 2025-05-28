import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Permissao:
    def __init__(self, id_permissao=None, nome="", descricao=""):
        self.id_permissao = id_permissao
        self.nome = nome
        self.descricao = descricao









# CREATE TABLE PERMISSAO (
# ID_PERMISSAO INT PRIMARY KEY AUTO_INCREMENT,
# NOME VARCHAR(50) NOT NULL UNIQUE,
# DESCRICAO TEXT NOT NULL