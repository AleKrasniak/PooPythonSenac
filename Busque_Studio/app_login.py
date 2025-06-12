# app_principal.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from app_cliente import AppCliente
from app_estudio import AppEstudio
from app_admin import AppAdmin
import mysql.connector
from clienteDAO import ClienteDAO

class AppLogin:
    """Classe para a janela de login separada"""
    def __init__(self, parent, callback_sucesso):
        self.parent = parent
        self.callback_sucesso = callback_sucesso
        self.dao = ClienteDAO()
        
        # Criar janela de login - AUMENTADA
        self.janela = tk.Toplevel(parent)
        self.janela.title("BusqueStudios - Login")
        self.janela.geometry("500x400")  # Aumentado de 400x300 para 500x400
        self.janela.configure(bg='#34495e')
        self.janela.resizable(False, False)
        
        # Centralizar janela
        self.centralizar_janela()
        
        # Tornar modal
        self.janela.transient(parent)
        self.janela.grab_set()
        
        self.criar_interface_login()
        
    def centralizar_janela(self):
        """Centraliza a janela de login na tela"""
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)  # Ajustado para nova largura
        y = (self.janela.winfo_screenheight() // 2) - (400 // 2)  # Ajustado para nova altura
        self.janela.geometry(f"500x400+{x}+{y}")
        
    def criar_interface_login(self):
        """Cria a interface da janela de login"""
        # Título - mais espaçamento
        titulo = tk.Label(self.janela, text="FAZER LOGIN", 
                         font=('Arial', 24, 'bold'),  # Fonte maior
                         bg='#34495e', fg='white')
        titulo.pack(pady=(40, 50))  # Mais espaçamento
        
        # Frame para campos - mais espaçoso
        frame_campos = tk.Frame(self.janela, bg='#34495e')
        frame_campos.pack(pady=30)
        
        # Campo Login
        tk.Label(frame_campos, text="Login:", 
                font=('Arial', 14, 'bold'),  # Fonte maior
                bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=15)
        
        self.entry_login = tk.Entry(frame_campos, width=30, font=('Arial', 14))  # Maior e fonte maior
        self.entry_login.grid(row=0, column=1, pady=15, padx=(20, 0))
        
        # Campo Senha
        tk.Label(frame_campos, text="Senha:", 
                font=('Arial', 14, 'bold'),  # Fonte maior
                bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=15)
        
        self.entry_senha = tk.Entry(frame_campos, width=30, font=('Arial', 14), show='*')  # Maior e fonte maior
        self.entry_senha.grid(row=1, column=1, pady=15, padx=(20, 0))
        
        # Frame para botões
        frame_botoes = tk.Frame(self.janela, bg='#34495e')
        frame_botoes.pack(pady=40)  # Mais espaçamento
        
        # Botão Entrar - maior
        btn_entrar = tk.Button(frame_botoes, text="ENTRAR", 
                              command=self.fazer_login,
                              bg='#27ae60', fg='white',
                              font=('Arial', 14, 'bold'),  # Fonte maior
                              width=15, height=2,  # Mais largo
                              cursor='hand2')
        btn_entrar.grid(row=0, column=0, padx=15)
        
        # Botão Cancelar - maior
        btn_cancelar = tk.Button(frame_botoes, text="CANCELAR", 
                                command=self.janela.destroy,
                                bg='#e74c3c', fg='white',
                                font=('Arial', 14, 'bold'),  # Fonte maior
                                width=15, height=2,  # Mais largo
                                cursor='hand2')
        btn_cancelar.grid(row=0, column=1, padx=15)
        
        # Bind Enter para fazer login
        self.entry_senha.bind('<Return>', lambda event: self.fazer_login())
        self.entry_login.bind('<Return>', lambda event: self.entry_senha.focus())
        
        # Focar no campo login
        self.entry_login.focus()
        
    def fazer_login(self):
        """Realiza o login do usuário"""
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha!", parent=self.janela)
            return
            
        try:
            # Busca usuário no banco de dados
            usuario = self.validar_credenciais(login, senha)
            
            if usuario:
                self.janela.destroy()  # Fecha janela de login
                self.callback_sucesso(usuario)  # Chama callback com dados do usuário
            else:
                messagebox.showerror("Erro", "Login ou senha incorretos!", parent=self.janela)
                self.limpar_campos()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}", parent=self.janela)
    
    def validar_credenciais(self, login, senha):
        """Valida as credenciais do usuário no banco de dados"""
        try:
            cursor = self.dao.cursor
            
            # Query para buscar usuário com login e senha
            query = """
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, 
                       p.nome_perfil, c.id_perfil
                FROM cliente c
                INNER JOIN perfil p ON c.id_perfil = p.id_perfil
                WHERE c.login = %s AND c.senha = %s
            """
            
            cursor.execute(query, (login, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    'id_cliente': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'telefone': resultado[3],
                    'cpf': resultado[4],
                    'nome_perfil': resultado[5],
                    'id_perfil': resultado[6]
                }
            return None
            
        except Exception as e:
            print(f"Erro na validação: {e}")
            return None
    
    def limpar_campos(self):
        """Limpa os campos de login"""
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_login.focus()