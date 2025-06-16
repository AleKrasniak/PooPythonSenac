import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Perfil:
    def __init__(self, id_perfil=None, nome="", descricao="" ):
        self.id_perfil = id_perfil
        self.nome = nome
        self.descricao = descricao
        
