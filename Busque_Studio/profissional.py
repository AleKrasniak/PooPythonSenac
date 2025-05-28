import tkinter as tk
from tkinter import messagebox
import mysql.connector
from estudio import Estudio

class Profissional:
    def __init__(self, id_profissional=None, id_estudio=None, nome="", cpf="", especialidade=""):
        self.id_profissional = id_profissional
        self.id_estudio = id_estudio
        self.nome = nome
        self.cpf = cpf
        self.especialidade= especialidade






# CREATE TABLE PROFISSIONAL(
# ID_PROFISSIONAL INT PRIMARY KEY AUTO_INCREMENT,
# ID_ESTUDIO INT NOT NULL,
# NOME VARCHAR(70) NOT NULL,
# CPF CHAR(11) NOT NULL UNIQUE,
# ESPECIALIDADE VARCHAR(40) NOT NULL,
# FOREIGN KEY (ID_ESTUDIO) REFERENCES ESTUDIO(ID_ESTUDIO)
# ON UPDATE CASCADE
# ON DELETE CASCADE
