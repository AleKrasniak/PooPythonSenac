import tkinter as tk
from tkinter import messagebox
import mysql.connector
from perfil import Perfil

class Administrador: 
    def __init__(self, id_administrador=None, id_perfil=None, nome="", email="", login="", senha=""):
        self.id_administrador = id_administrador
        self.id_perfil = id_perfil
        self.nome = nome
        self.email = email
        self.login = login
        self.senha = senha





# CREATE TABLE ADMINISTRADOR(
# ID_ADMINISTRADOR INT PRIMARY KEY AUTO_INCREMENT,
# ID_PERFIL INT NOT NULL,
# NOME VARCHAR(70) NOT NULL,
# EMAIL VARCHAR(70) NOT NULL,
# LOGIN VARCHAR(20) NOT NULL,
# SENHA VARCHAR(150) NOT NULL,
# FOREIGN KEY (ID_PERFIL) REFERENCES PERFIL(ID_PERFIL)
# ON UPDATE CASCADE
# ON DELETE CASCADE