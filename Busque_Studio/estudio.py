import tkinter as tk
from tkinter import messagebox
import mysql.connector
from perfil import Perfil
from endereco import Endereco 

class Estudio:
    def __init__(self, id_estudio=None, id_perfil=None, id_endereco=None, nome="", cnpj="", descricao="", login="", senha="", tipo="" ):
        self.id_estudio = id_estudio
        self.id_perfil = id_perfil
        self.id_endereco = id_endereco
        self.nome = nome 
        self.cnpj = cnpj
        self.descricao = descricao
        self.login = login
        self.senha = senha
        self.tipo = tipo




# CREATE TABLE ESTUDIO(   FAZER PORTFÓLIO
# ID_ESTUDIO INT PRIMARY KEY AUTO_INCREMENT,
# ID_PERFIL INT NOT NULL,
# ID_ENDERECO INT NOT NULL,
# NOME VARCHAR(100) NOT NULL,
# CNPJ CHAR(14) NOT NULL UNIQUE,
# DESCRICAO VARCHAR(250) NOT NULL,
# LOGIN VARCHAR(20) NOT NULL UNIQUE,
# SENHA VARCHAR(150) NOT NULL,
# TIPO VARCHAR(50),
# FOREIGN KEY (ID_PERFIL) REFERENCES PERFIL(ID_PERFIL)
# ON UPDATE CASCADE
# ON DELETE RESTRICT,
# FOREIGN KEY (ID_ENDERECO) REFERENCES ENDERECO(ID_ENDERECO)
# ON UPDATE CASCADE
# ON DELETE CASCADE