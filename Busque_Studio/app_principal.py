# app_principal.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from app_cliente import AppCliente
from app_estudio import AppEstudio
from app_admin import AppAdmin

class AppPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BusqueStudios - Sistema Principal")
        self.root.geometry("400x300")
        self.root.configure(bg='#2c3e50')
        
        self.criar_interface()
        
    def criar_interface(self):
        # Logo/Título
        titulo = tk.Label(self.root, text="BUSQUE STUDIOS", 
                         font=('Arial', 24, 'bold'), 
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=30)
        
        subtitulo = tk.Label(self.root, text="Sistema de Gestão", 
                            font=('Arial', 12), 
                            bg='#2c3e50', fg='#bdc3c7')
        subtitulo.pack(pady=(0, 40))
        
        # Frame para botões
        frame_botoes = tk.Frame(self.root, bg='#2c3e50')
        frame_botoes.pack(expand=True)
        
        # Botão Cadastrar Cliente - PERFIL ID = 1 (CLIENTE)
        btn_cliente = tk.Button(frame_botoes, 
                               text="CADASTRAR CLIENTE",
                               command=self.abrir_cadastro_cliente,
                               bg='#3498db', fg='white',
                               font=('Arial', 14, 'bold'),
                               width=20, height=2,
                               cursor='hand2')
        btn_cliente.pack(pady=10)
        
        # Botão Cadastrar Estúdio - PERFIL ID = 2 (ESTÚDIO)
        btn_estudio = tk.Button(frame_botoes, 
                               text="CADASTRAR ESTÚDIO",
                               command=self.abrir_cadastro_estudio,
                               bg='#e74c3c', fg='white',
                               font=('Arial', 14, 'bold'),
                               width=20, height=2,
                               cursor='hand2')
        btn_estudio.pack(pady=10)
        
        # Botão Admin - PERFIL ID = 3 (ADMIN)
        btn_admin = tk.Button(frame_botoes, 
                             text="ÁREA ADMINISTRATIVA",
                             command=self.abrir_area_admin,
                             bg='#95a5a6', fg='white',
                             font=('Arial', 10),
                             width=20, height=1,
                             cursor='hand2')
        btn_admin.pack(pady=(30, 10))
        
    def abrir_cadastro_cliente(self):
        """
        PERFIL AUTOMÁTICO: Cliente sempre recebe perfil_id=1 (Cliente)
        Não pode escolher perfil - é definido automaticamente!
        """
        self.root.withdraw()  # Esconde a tela principal
        
        # Cria nova janela com PERFIL FIXO = CLIENTE
        janela_cliente = tk.Toplevel()
        app_cliente = AppCliente(janela_cliente)
        
        # Quando fechar, volta para tela principal
        janela_cliente.protocol("WM_DELETE_WINDOW", self.fechar_janela_secundaria)
        
    def abrir_cadastro_estudio(self):
        """
        PERFIL AUTOMÁTICO: Estúdio sempre recebe perfil_id=2 (Estúdio)
        Não pode escolher perfil - é definido automaticamente!
        """
        self.root.withdraw()  # Esconde a tela principal
        
        # Cria nova janela com PERFIL FIXO = ESTÚDIO
        janela_estudio = tk.Toplevel()
        app_estudio = AppEstudio(janela_estudio)
        
        # Quando fechar, volta para tela principal
        janela_estudio.protocol("WM_DELETE_WINDOW", self.fechar_janela_secundaria)
        
    def abrir_area_admin(self):
        """
        PERFIL AUTOMÁTICO: Admin sempre recebe perfil_id=3 (Admin)
        Pode ver/editar todos os cadastros (modo_admin=True)
        """
        # Pede senha de administrador
        senha = simpledialog.askstring("Acesso Restrito", 
                                      "Digite a senha de administrador:", 
                                      show='*')
        
        if senha == "admin123":  # Senha fixa (em produção, use hash)
            self.root.withdraw()
            
            # Cria janela com PERFIL FIXO = ADMIN + MODO ADMIN ATIVADO
            janela_admin = tk.Toplevel()
            app_admin = AppAdmin(janela_admin)
            janela_admin.protocol("WM_DELETE_WINDOW", self.fechar_janela_secundaria)
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
    
    def fechar_janela_secundaria(self):
        """Volta para tela principal ao fechar qualquer janela secundária"""
        self.root.deiconify()  # Mostra a tela principal novamente
        
    def executar(self):
        self.root.mainloop()