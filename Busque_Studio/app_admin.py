import tkinter as tk
from tkinter import messagebox, ttk
from clienteDAO import ClienteDAO
from botao_voltar import criar_botao_voltar  # <- IMPORTAÇÃO CERTA

class AppAdmin:
    def __init__(self, parent_janela):
        self.parent = parent_janela
        self.janela = tk.Toplevel()
        self.janela.title("BusqueStudios - Administrador")
        self.janela.geometry("800x600")
        self.janela.configure(bg='#e74c3c')
        self.janela.resizable(False, False)
        self.centralizar_janela()
        
        self.janela.transient(parent_janela)
        self.janela.grab_set()
        
        self.criar_interface()
    
    def centralizar_janela(self):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (600 // 2)
        self.janela.geometry(f"800x600+{x}+{y}")
    
    def criar_interface(self):
        titulo = tk.Label(self.janela, text="PAINEL ADMINISTRATIVO",
                         font=('Arial', 24, 'bold'),
                         bg='#e74c3c', fg='white')
        titulo.pack(pady=50)
        
        criar_botao_voltar(self.janela, self.voltar)
        
        frame_botoes = tk.Frame(self.janela, bg='#e74c3c')
        frame_botoes.pack(pady=50)
        
        tk.Button(frame_botoes, text="GERENCIAR USUÁRIOS",
                 bg='#34495e', fg='white',
                 font=('Arial', 14, 'bold'),
                 width=20, height=3,
                 cursor='hand2',
                 command=self.gerenciar_usuarios).pack(pady=20)
        
        tk.Button(frame_botoes, text="RELATÓRIOS",
                 bg='#16a085', fg='white',
                 font=('Arial', 14, 'bold'),
                 width=20, height=3,
                 cursor='hand2',
                 command=self.relatorios).pack(pady=20)
    
    def gerenciar_usuarios(self):
        messagebox.showinfo("Info", "Gerenciar usuários em desenvolvimento", parent=self.janela)
    
    def relatorios(self):
        messagebox.showinfo("Info", "Relatórios em desenvolvimento", parent=self.janela)
    
    def voltar(self):
        self.janela.destroy()