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

        
        



# CREATE TABLE CLIENTE(
# ID_CLIENTE INT PRIMARY KEY AUTO_INCREMENT,
# ID_PERFIL INT NOT NULL,
# ID_ENDERECO INT NOT NULL,
# NOME VARCHAR(70) NOT NULL,
# DT_NASC DATE NOT NULL,
# GENERO ENUM ('Masculino','Feminino') NOT NULL,
# TELEFONE VARCHAR(20),
# CPF CHAR(11) NOT NULL UNIQUE,
# EMAIL VARCHAR(150) NOT NULL UNIQUE,
# LOGIN VARCHAR(20) NOT NULL UNIQUE,
# SENHA VARCHAR(150) NOT NULL,
# FOREIGN KEY (ID_PERFIL) REFERENCES PERFIL(ID_PERFIL)
# ON UPDATE CASCADE
# ON DELETE CASCADE,
# FOREIGN KEY (ID_ENDERECO) REFERENCES ENDERECO(ID_ENDERECO)
# ON UPDATE CASCADE
# ON DELETE CASCADE
