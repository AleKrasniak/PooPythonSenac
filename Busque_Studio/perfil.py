import tkinter as tk
from tkinter import messagebox
import mysql.connector


class Perfil:
    def __init__(self, id_perfil=None, nome="", descricao="" ):
        self.id_perfil = id_perfil
        self.nome = nome
        self.descricao = descricao
        



# ID_PERFIL INT PRIMARY KEY AUTO_INCREMENT,
# NOME VARCHAR(50) NOT NULL COMMENT 'Administrador, Cliente, Estudio',
# DESCRICAO VARCHAR(100)
# );