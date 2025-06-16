import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, date
from estudio import Estudio

class Alvara:
    def __init__(self, id_alvara=None, id_estudio=None, numero_alvara=None, 
                 tipo_alvara=None, data_emissao=None, data_validade=None, 
                 status='ativo', descricao=None, documento_anexo=None, 
                 criado_em=None, atualizado_em=None):
        self.id_alvara = id_alvara
        self.id_estudio = id_estudio
        self.numero_alvara = numero_alvara
        self.tipo_alvara = tipo_alvara
        self.data_emissao = data_emissao
        self.data_validade = data_validade
        self.status = status
        self.descricao = descricao
        self.documento_anexo = documento_anexo
        self.criado_em = criado_em or datetime.now()
        self.atualizado_em = atualizado_em or datetime.now()