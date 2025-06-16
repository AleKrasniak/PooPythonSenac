import tkinter as tk
from tkinter import messagebox
import mysql.connector
# from perfil import Perfil
# from endereco import Endereco

class ClienteDAO:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        self.cursor = self.conexao.cursor()

    def criar(self, cliente):
        sql = "INSERT INTO cliente (id_perfil, id_endereco, nome, dt_nasc, genero, telefone, cpf, email, login, senha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (cliente.id_perfil, cliente.id_endereco, cliente.nome, cliente.dt_nasc, cliente.genero, cliente.telefone, cliente.cpf, cliente.email, cliente.login, cliente.senha))
        self.conexao.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM cliente")
        return self.cursor.fetchall()
    
    def atualizar(self, cliente):
        sql = "UPDATE cliente SET id_perfil = %s, id_endereco = %s, nome = %s, dt_nasc = %s, genero = %s, telefone = %s, cpf = %s, email = %s, login = %s, senha = %s WHERE id_cliente = %s"
        self.cursor.execute(sql, (cliente.id_perfil, cliente.id_endereco, cliente.nome, cliente.dt_nasc, cliente.genero, cliente.telefone, cliente.cpf, cliente.email, cliente.login, cliente.senha, cliente.id_cliente))
        self.conexao.commit()

    def deletar(self, id_cliente):
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        self.cursor.execute(sql, (id_cliente,))
        self.conexao.commit()

    def buscar_por_id(self, id_cliente):
        """Método para buscar cliente por ID"""
        sql = "SELECT * FROM cliente WHERE id_cliente = %s"
        self.cursor.execute(sql, (id_cliente,))
        return self.cursor.fetchone()

    def buscar_cliente_com_endereco(self, id_cliente):
        """Método para buscar cliente com dados do endereço (incluindo UF)"""
        sql = """
        SELECT c.*, e.uf, e.cidade, e.bairro, e.rua, e.numero, e.cep 
        FROM cliente c 
        LEFT JOIN endereco e ON c.id_endereco = e.id_endereco 
        WHERE c.id_cliente = %s
        """
        self.cursor.execute(sql, (id_cliente,))
        return self.cursor.fetchone()

    def listar_clientes_com_endereco(self):
        """Método para listar todos os clientes com dados do endereço (incluindo UF)"""
        sql = """
        SELECT c.*, e.uf, e.cidade, e.bairro, e.rua, e.numero, e.cep 
        FROM cliente c 
        LEFT JOIN endereco e ON c.id_endereco = e.id_endereco
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def buscar_por_login(self, login, senha):
        """Método para buscar cliente por login e senha"""
        sql = "SELECT * FROM cliente WHERE login = %s AND senha = %s"
        self.cursor.execute(sql, (login, senha))
        return self.cursor.fetchone()

    def buscar_por_login_com_endereco(self, login, senha):
        """Método para buscar cliente por login e senha com dados do endereço"""
        sql = """
        SELECT c.*, e.uf, e.cidade, e.bairro, e.rua, e.numero, e.cep 
        FROM cliente c 
        LEFT JOIN endereco e ON c.id_endereco = e.id_endereco 
        WHERE c.login = %s AND c.senha = %s
        """
        self.cursor.execute(sql, (login, senha))
        return self.cursor.fetchone()

    def buscar_por_cpf(self, cpf):
        """Método para buscar cliente por CPF (útil para validar duplicatas)"""
        sql = "SELECT * FROM cliente WHERE cpf = %s"
        self.cursor.execute(sql, (cpf,))
        return self.cursor.fetchone()

    def buscar_por_email(self, email):
        """Método para buscar cliente por email (útil para validar duplicatas)"""
        sql = "SELECT * FROM cliente WHERE email = %s"
        self.cursor.execute(sql, (email,))
        return self.cursor.fetchone()

    def buscar_por_login_disponivel(self, login):
        """Método para verificar se um login está disponível"""
        sql = "SELECT COUNT(*) FROM cliente WHERE login = %s"
        self.cursor.execute(sql, (login,))
        resultado = self.cursor.fetchone()
        return resultado[0] == 0  # Retorna True se login está disponível

    def fechar_conexao(self):
        """Método para fechar a conexão"""
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()