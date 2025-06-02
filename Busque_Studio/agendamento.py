import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cliente import Cliente
from estudio import Estudio
from profissional import Profissional
from datetime import datetime 

class Agendamento:
    def __init__(self, id_agendamento=None, id_cliente=None, id_estudio=None, id_profissional=None, data_hora=None, valor=None, status="Agendado"):
        self.id_agendamento = id_agendamento
        self.id_cliente = id_cliente
        self.id_estudio = id_estudio
        self.id_profissional = id_profissional
        self.data_hora = data_hora or datetime.now()
        self.valor = valor
        self.status = status







# CREATE TABLE AGENDAMENTO(
# ID INT PRIMARY KEY AUTO_INCREMENT,
# ID_CLIENTE INT NOT NULL,
# ID_ESTUDIO INT NOT NULL,
# ID_PROFISSIONAL INT NOT NULL,
# DATA_HORA DATETIME NOT NULL,
# VALOR DECIMAL(10,2),
# STATUS ENUM('Agendado', 'Confirmado', 'Cancelado', 'Atendido', 'Concluído') DEFAULT 'Agendado',
# FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE),
# FOREIGN KEY (ID_ESTUDIO) REFERENCES ESTUDIO(ID_ESTUDIO),
# FOREIGN KEY (ID_PROFISSIONAL) REFERENCES PROFISSIONAL(ID_PROFISSIONAL)