import tkinter as tk
from tkinter import messagebox
import mysql.connector
from perfil import Perfil
from endereco import Endereco

class Cliente:
    def __init__(self, id_cliente=None, id_perfil=None, id_endereco=None, nome="", dt_nasc="", genero="", telefone="", cpf="", email="", login="", senha=""):
        self.id_cliente = id_cliente
        self.id_perfil = id_perfil
        self.id_endereco = id_endereco
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.genero = genero
        self.telefone = telefone 
        self.cpf = cpf 
        self.email = email
        self.login = login
        self.senha = senha

        
        

