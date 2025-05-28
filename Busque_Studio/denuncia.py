import tkinter as tk
from tkinter import messagebox
import mysql.connector
from cliente import Cliente
from estudio import Estudio
from datetime import datetime 
class Denuncia:
    def __init__(self, id_denuncia=None, id_cliente=None, id_estudio=None, motivo="", status="Pendente", data_criacao=None, foto_caminho="", foto_nome_arquivo="", data_atualizacao=None):
        self.id_denuncia = id_denuncia
        self.id_cliente = id_cliente
        self.id_estudio = id_estudio
        self.motivo= motivo
        self.status = status
        self.data_criacao = data_criacao or datetime.now()
        self.foto_caminho = foto_caminho
        self.foto_nome_arquivo = foto_nome_arquivo
        self.data_atualizacao = data_atualizacao or datetime.now()









# CREATE TABLE DENUNCIA(
# ID_DENUNCIA INT PRIMARY KEY AUTO_INCREMENT,
# ID_CLIENTE INT,
# ID_ESTUDIO INT,
# MOTIVO VARCHAR(250),
# STATUS ENUM('Pendente','Em análise', 'Aceita', 'Rejeitado', 'Resolvida') DEFAULT 'Pendente',
# DATA_CRIACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# FOTO_CAMINHO VARCHAR(255) COMMENT 'Caminho URL da foto',
# FOTO_NOME_ARQUIVO VARCHAR(100) COMMENT 'Nome do arquivo',
# DATA_ATUALIZACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# FOREIGN KEY (ID_CLIENTE) REFERENCES CLIENTE(ID_CLIENTE)
# ON UPDATE CASCADE
# ON DELETE SET NULL,
# FOREIGN KEY (ID_ESTUDIO) REFERENCES ESTUDIO(ID_ESTUDIO)
# ON UPDATE CASCADE
# ON DELETE SET NULL