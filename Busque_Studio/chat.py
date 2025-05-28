import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cliente import Cliente
from estudio import Estudio
from datetime import datetime 

class Chat:
    def __init__(self, id_chat=None, data_inicio=None, id_cliente=None, id_estudio=None):
        self.id_chat = id_chat
        self.data_inicio = data_inicio or datetime.now()
        self.id_cliente = id_cliente
        self.id_estudio = id_estudio

# CREATE TABLE CHAT(
# ID_CHAT INT PRIMARY KEY AUTO_INCREMENT,
# DATA_INICIO DATETIME DEFAULT CURRENT_TIMESTAMP,
# ID_CLIENTE INT,
# ID_ESTUDIO INT,
# FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
# ON UPDATE CASCADE
# ON DELETE SET NULL,
# FOREIGN KEY (ID_ESTUDIO) REFERENCES ESTUDIO(ID_ESTUDIO)
# ON UPDATE CASCADE
# ON DELETE SET NULL