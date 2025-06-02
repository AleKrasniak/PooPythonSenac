import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mensagem import Mensagem

class Mensagemmidia:
    def __init__(self, id_mensagem_midia=None, id_mensagem=None, url="", tipo=""):
        self.id_mensagem_midia = id_mensagem_midia
        self.id_mensagem = id_mensagem
        self.url = url
        self.tipo = tipo
        



# CREATE TABLE MENSAGEM_MIDIA(
# ID INT PRIMARY KEY AUTO_INCREMENT,
# ID_MENSAGEM INT NOT NULL,
# URL VARCHAR(255) NOT NULL,
# TIPO ENUM('Imagem','Video','Documento'),
# FOREIGN KEY (ID_MENSAGEM) REFERENCES MENSAGEM(ID_MENSAGEM)
# ON DELETE CASCADE