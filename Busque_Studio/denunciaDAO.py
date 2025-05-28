import tkinter as tk
from tkinter import messagebox
import mysql.connector

class DenunciaDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, denuncia):
        sql = "INSERTO INTO denuncia (id_cliente, id_estudio, motivo, status, data_criacao, foto_caminho, foto_nome_arquivo, data_atualizacao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (denuncia.id_cliente, denuncia.id_estudio, denuncia.motivo, denuncia.status, denuncia.data_criacao, denuncia.foto_caminho, denuncia.foto_nome_arquivo, denuncia.data_atualizacao))
    
    def listar(self):
        self.cursor.execute("SELECT * FROM denuncia")
        return self.cursor.fetchall()
    
    def atualizar(self, denuncia):
        sql = "UPDATE denuncia SET id_cliente = %s, id_estudio = %s, motivo = %s, status = %s, data_criacao = %s, foto_caminho = %s, foto_nome_arquivo = %s, data_atualizacao = %s WHERE id_denuncia = %s"
        self.cursor.execute(sql,(denuncia.id_cliente, denuncia.id_estudio, denuncia.motivo, denuncia.status, denuncia.data_criacao, denuncia.foto_caminho, denuncia.foto_nome_arquivo, denuncia.data_atualizacao, denuncia.id_denuncia))
        self.conexao.commit()

    def deletar(self, id_denuncia):
        sql= "DELETE FROM denuncia WHERE id_denuncia %s"
        self.cursor.execute(sql,(id_denuncia,))
        self.conexao.commit()




 







    # def __init__(self, id_denuncia=None, id_cliente=None, id_estudio=None, motivo="", status="Pendente", data_criacao=None, foto_caminho="", foto_nome_arquivo="", data_atualizacao=None):
    #     self.id_denuncia = id_denuncia
    #     self.id_cliente = id_cliente
    #     self.id_estudio = id_estudio
    #     self.motivo= motivo
    #     self.status = status
    #     self.data_criacao = data_criacao or datetime.now()
    #     self.foto_caminho = foto_caminho
    #     self.foto_nome_arquivo = foto_nome_arquivo
    #     self.data_atualizacao = data_atualizacao or datetime.now()