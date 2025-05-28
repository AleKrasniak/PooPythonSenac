import tkinter as tk
from tkinter import messagebox
import mysql.connector

class Usuario:
    def __init__(self, id=None, nome="", email=""):
        self.id = id 
        self.nome = nome
        self.email = email 