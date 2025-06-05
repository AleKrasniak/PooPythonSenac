# app_principal.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from app_cliente import AppCliente
from app_estudio import AppEstudio
from app_admin import AppAdmin
from app_login import AppLogin  # Replace with actual module name
import mysql.connector
from clienteDAO import ClienteDAO

class AppPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BusqueStudios - Sistema Principal")
        self.root.geometry("400x400")
        self.root.configure(bg='#2c3e50')
        
        self.usuario_logado = None
        
        self.criar_interface()
        
    def criar_interface(self):
        # Logo/Título
        titulo = tk.Label(self.root, text="BUSQUE STUDIOS", 
                         font=('Arial', 24, 'bold'), 
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=30)
        
        separador = tk.Label(self.root, text="LOGIN", 
                            font=('Arial', 12, 'bold'), 
                            bg='#2c3e50', fg='#bdc3c7')
        separador.pack(pady=20)
        
        # Frame para botões principais
        frame_botoes = tk.Frame(self.root, bg='#2c3e50')
        frame_botoes.pack(expand=True)
        
        # Botão ENTRAR - Abre janela de login
        btn_entrar = tk.Button(frame_botoes, 
                              text="ENTRAR",
                              command=self.abrir_janela_login,
                              bg='#27ae60', fg='white',
                              font=('Arial', 16, 'bold'),
                              width=18, height=2,
                              cursor='hand2')
        btn_entrar.pack(pady=15)
        
        # Separador
        separador = tk.Label(self.root, text="OU CADASTRE-SE", 
                            font=('Arial', 12, 'bold'), 
                            bg='#2c3e50', fg='#bdc3c7')
        separador.pack(pady=20)
        
        # Frame para botões de cadastro
        frame_cadastro = tk.Frame(self.root, bg='#2c3e50')
        frame_cadastro.pack()
        
        # Botão Cadastrar Cliente
        btn_cliente = tk.Button(frame_cadastro, 
                               text="CADASTRAR CLIENTE",
                               command=self.abrir_cadastro_cliente,
                               bg='#BA4467', fg='white',
                               font=('Arial', 12, 'bold'),
                               width=20, height=2,
                               cursor='hand2')
        btn_cliente.pack(pady=8)
        
        # Botão Cadastrar Estúdio
        btn_estudio = tk.Button(frame_cadastro, 
                               text="CADASTRAR ESTÚDIO",
                               command=self.abrir_cadastro_estudio,
                               bg='#e74c3c', fg='white',
                               font=('Arial', 12, 'bold'),
                               width=20, height=2,
                               cursor='hand2')
        btn_estudio.pack(pady=8)
        
        # Botão Admin
        btn_admin = tk.Button(frame_cadastro, 
                             text="ÁREA ADMINISTRATIVA",
                             command=self.abrir_area_admin,
                             bg='#95a5a6', fg='white',
                             font=('Arial', 10),
                             width=20, height=1,
                             cursor='hand2')
        btn_admin.pack(pady=(20, 10))
        
    def abrir_janela_login(self):
        """Abre a janela de login separada"""
        AppLogin(self.root, self.login_realizado_com_sucesso)
        
    def login_realizado_com_sucesso(self, usuario):
        """Callback chamado quando login é realizado com sucesso"""
        self.usuario_logado = usuario
        self.mostrar_area_logado()
        
    def mostrar_area_logado(self):
        """Mostra a área do usuário logado"""
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("500x400")
        
        # Header com informações do usuário
        frame_header = tk.Frame(self.root, bg='#27ae60', height=80)
        frame_header.pack(fill='x')
        frame_header.pack_propagate(False)
        
        tk.Label(frame_header, text=f"Bem-vindo(a), {self.usuario_logado['nome']}!", 
                font=('Arial', 16, 'bold'), 
                bg='#27ae60', fg='white').pack(pady=10)
        
        tk.Label(frame_header, text=f"Perfil: {self.usuario_logado['nome_perfil']}", 
                font=('Arial', 12), 
                bg='#27ae60', fg='white').pack()
        
        # Frame principal
        frame_main = tk.Frame(self.root, bg='#f0f0f0')
        frame_main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Opções baseadas no perfil
        self.criar_opcoes_perfil(frame_main)
        
        # Botão logout
        btn_logout = tk.Button(frame_main, text="SAIR", 
                              command=self.fazer_logout,
                              bg='#e74c3c', fg='white',
                              font=('Arial', 10, 'bold'),
                              width=15, height=2)
        btn_logout.pack(side='bottom', pady=20)
    
    def criar_opcoes_perfil(self, frame_parent):
        """Cria opções específicas baseadas no perfil do usuário"""
        perfil_id = self.usuario_logado['id_perfil']
        
        if perfil_id == 1:  # Cliente
            tk.Label(frame_parent, text="ÁREA DO CLIENTE", 
                    font=('Arial', 18, 'bold'), 
                    bg='#f0f0f0', fg='#BA4467').pack(pady=20)
            
            btn_perfil = tk.Button(frame_parent, text="Meu Perfil", 
                                  command=self.abrir_meu_perfil,
                                  bg='#BA4467', fg='white',
                                  font=('Arial', 12, 'bold'),
                                  width=20, height=2)
            btn_perfil.pack(pady=10)
            
            btn_buscar = tk.Button(frame_parent, text="Buscar Estúdios", 
                                  command=self.buscar_estudios,
                                  bg='#3498db', fg='white',
                                  font=('Arial', 12, 'bold'),
                                  width=20, height=2)
            btn_buscar.pack(pady=10)
            
        elif perfil_id == 2:  # Estúdio
            tk.Label(frame_parent, text="ÁREA DO ESTÚDIO", 
                    font=('Arial', 18, 'bold'), 
                    bg='#f0f0f0', fg='#e74c3c').pack(pady=20)
            
            btn_perfil = tk.Button(frame_parent, text="Meu Perfil", 
                                  command=self.abrir_meu_perfil,
                                  bg='#e74c3c', fg='white',
                                  font=('Arial', 12, 'bold'),
                                  width=20, height=2)
            btn_perfil.pack(pady=10)
            
            btn_servicos = tk.Button(frame_parent, text="Meus Serviços", 
                                    command=self.gerenciar_servicos,
                                    bg='#f39c12', fg='white',
                                    font=('Arial', 12, 'bold'),
                                    width=20, height=2)
            btn_servicos.pack(pady=10)
            
        elif perfil_id == 3:  # Admin
            tk.Label(frame_parent, text="ÁREA ADMINISTRATIVA", 
                    font=('Arial', 18, 'bold'), 
                    bg='#f0f0f0', fg='#95a5a6').pack(pady=20)
            
            btn_admin_panel = tk.Button(frame_parent, text="Painel Administrativo", 
                                       command=self.abrir_painel_admin,
                                       bg='#95a5a6', fg='white',
                                       font=('Arial', 12, 'bold'),
                                       width=20, height=2)
            btn_admin_panel.pack(pady=10)
    
    def abrir_meu_perfil(self):
        """Abre tela de perfil do usuário"""
        messagebox.showinfo("Em Desenvolvimento", 
                           "Funcionalidade 'Meu Perfil' será implementada em breve!")
    
    def buscar_estudios(self):
        """Abre tela de busca de estúdios para clientes"""
        messagebox.showinfo("Em Desenvolvimento", 
                           "Funcionalidade 'Buscar Estúdios' será implementada em breve!")
    
    def gerenciar_servicos(self):
        """Abre tela de gerenciamento de serviços para estúdios"""
        messagebox.showinfo("Em Desenvolvimento", 
                           "Funcionalidade 'Meus Serviços' será implementada em breve!")
    
    def abrir_painel_admin(self):
        """Abre painel administrativo"""
        janela_admin = tk.Toplevel()
        app_admin = AppAdmin(janela_admin)
        janela_admin.protocol("WM_DELETE_WINDOW", 
                             lambda: janela_admin.destroy())
    
    def fazer_logout(self):
        """Faz logout do usuário"""
        self.usuario_logado = None
        
        # Limpa a tela e recria interface inicial
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("400x400")
        self.criar_interface()
        messagebox.showinfo("Logout", "Logout realizado com sucesso!")
        
    def abrir_cadastro_cliente(self):
        """Abre cadastro de cliente"""
        self.root.withdraw()
        janela_cliente = tk.Toplevel()
        app_cliente = AppCliente(janela_cliente)
        janela_cliente.protocol("WM_DELETE_WINDOW", self.fechar_janela_secundaria)
        
    def abrir_cadastro_estudio(self):
        """Abre cadastro de estúdio"""
        self.root.withdraw()
        janela_estudio = tk.Toplevel()
        app_estudio = AppEstudio(janela_estudio)
        janela_estudio.protocol("WM_DELETE_WINDOW", self.fechar_janela_secundaria)
        
    def abrir_area_admin(self):
        """Abre área administrativa com senha"""
        senha = simpledialog.askstring("Acesso Restrito", 
                                      "Digite a senha de administrador:", 
                                      show='*')
        
        if senha == "admin123":
            self.root.withdraw()
            janela_admin = tk.Toplevel()
            app_admin = AppAdmin(janela_admin)
            janela_admin.protocol("WM_DELETE_WINDOW", self.fechar_janela_secundaria)
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
    
    def fechar_janela_secundaria(self):
        """Volta para tela principal ao fechar janela secundária"""
        self.root.deiconify()
        
    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppPrincipal()
    app.executar()