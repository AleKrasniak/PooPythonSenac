import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

class Endereco:
    def __init__(self, id_endereco=None, rua="", numero=0, bairro="", cidade="", complemento="", uf="", cep="", data_cadastro=None, data_atualizacao=None ):
        self.id_endereco = id_endereco
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.complemento = complemento
        self.uf = uf 
        self.cep = cep
        self.data_cadastro = data_cadastro or datetime.now()
        self.data_atualizacao = data_atualizacao or datetime.now()

        











# CREATE TABLE ENDERECO(
# ID_ENDERECO INT PRIMARY KEY AUTO_INCREMENT,
# RUA VARCHAR(100),
# NUMERO INT,
# BAIRRO VARCHAR(50),
# CIDADE VARCHAR(70),
# COMPLEMENTO VARCHAR(150),
# UF VARCHAR(2) NOT NULL,
# CEP VARCHAR(9) NOT NULL
# COMMENT 'Formato: XXXXX-XXX'
# CHECK (CEP REGEXP '^[0-9]{5}-[0-9]{3}$'),
# DATA_CADASTRO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# DATA_ATUALIZACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# INDEX IDX_CEP (CEP)
# 