import tkinter as tk
from tkinter import messagebox
import mysql.connector
from chat import Chat
from datetime import datetime 

class Mensagem:
    def __init__(self, id_mensagem=None, id_chat=None, texto="", data_envio=None, remetente_tipo="", status="Enviada",):
        self.id_mensagem = id_mensagem
        self.id_chat = id_chat
        self.texto = texto
        self.data_envio = data_envio or datetime.now()
        self.remetente_tipo = remetente_tipo
        self.status = status
        



# CREATE TABLE MENSAGEM(
# ID_MENSAGEM INT PRIMARY KEY AUTO_INCREMENT,
# ID_CHAT INT NOT NULL,
# ID_REMETENTE INT NOT NULL,
# TEXTO VARCHAR(250),
# DATA_ENVIO DATETIME DEFAULT CURRENT_TIMESTAMP,
# REMETENTE_TIPO ENUM('Cliente','Estudio') NOT NULL,
# STATUS ENUM('Enviada','Entregue', 'Lida') DEFAULT 'Enviada',
# FOREIGN KEY (ID_CHAT) REFERENCES CHAT(ID_CHAT)