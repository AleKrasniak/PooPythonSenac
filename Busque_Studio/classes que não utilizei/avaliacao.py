import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cliente import Cliente
from estudio import Estudio
from datetime import datetime

class Avaliacao:
    def __init__(self, id_agendamento=None, id_cliente=None, id_estudio=None, nota=None, comentario="", data_avaliacao=None,):
        self.id_avaliacao = id_agendamento
        self.id_cliente = id_cliente
        self.id_estudio = id_estudio
        self.nota = nota
        self.comentario = comentario
        self.data_avalicao = data_avaliacao or datetime.now()







# CREATE TABLE AVALIACAO(
# ID INT PRIMARY KEY AUTO_INCREMENT,
# ID_CLIENTE INT NOT NULL,
# ID_ESTUDIO INT NOT NULL,
# NOTA DECIMAL(2,1) NOT NULL CHECK (NOTA BETWEEN 0 AND 5),
# COMENTARIO TEXT,
# DATA_AVALIACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
# ON UPDATE CASCADE
# ON DELETE CASCADE,
# FOREIGN KEY (ID_ESTUDIO) REFERENCES ESTUDIO(ID_ESTUDIO)
# ON UPDATE CASCADE
# ON DELETE CASCADE