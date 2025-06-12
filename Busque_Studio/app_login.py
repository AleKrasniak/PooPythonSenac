# app_principal.py - CORREÇÃO DO LOGIN
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from app_cliente import AppCliente
from app_estudio import AppEstudio
from app_admin import AppAdmin
import mysql.connector
from clienteDAO import ClienteDAO
import hashlib


class AppLogin:
    def __init__(self):
        # SOLUÇÃO DO PROBLEMA: Não criar janela pai oculta
        self.root = tk.Tk()
        self.root.title("BusqueStudios - Sistema de Login")
        self.root.geometry("600x500")
        self.root.configure(bg='#34495e')
        self.root.resizable(False, False)
        
        # Inicializar DAO
        self.dao = ClienteDAO()
        
        self.centralizar_janela()
        self.criar_interface_login()
        
        # Configurar fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
    
    def centralizar_janela(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
    
    def criar_interface_login(self):
        titulo = tk.Label(self.root, text="BUSQUE STUDIOS",
                         font=('Arial', 28, 'bold'),
                         bg='#34495e', fg='white')
        titulo.pack(pady=(40, 10))
        
        subtitulo = tk.Label(self.root, text="Sistema de Gestão de Estúdios",
                            font=('Arial', 12),
                            bg='#34495e', fg='#bdc3c7')
        subtitulo.pack(pady=(0, 40))
        
        frame_campos = tk.Frame(self.root, bg='#34495e')
        frame_campos.pack(pady=30)
        
        tk.Label(frame_campos, text="Login:",
                font=('Arial', 14, 'bold'),
                bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=15)
        
        self.entry_login = tk.Entry(frame_campos, width=30, font=('Arial', 14))
        self.entry_login.grid(row=0, column=1, pady=15, padx=(20, 0))
        
        tk.Label(frame_campos, text="Senha:",
                font=('Arial', 14, 'bold'),
                bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=15)
        
        self.entry_senha = tk.Entry(frame_campos, width=30, font=('Arial', 14), show='*')
        self.entry_senha.grid(row=1, column=1, pady=15, padx=(20, 0))
        
        frame_botoes = tk.Frame(self.root, bg='#34495e')
        frame_botoes.pack(pady=40)
        
        btn_entrar = tk.Button(frame_botoes, text="ENTRAR",
                              command=self.fazer_login,
                              bg='#27ae60', fg='white',
                              font=('Arial', 14, 'bold'),
                              width=15, height=2,
                              cursor='hand2')
        btn_entrar.grid(row=0, column=0, padx=15)
        
        btn_sair = tk.Button(frame_botoes, text="SAIR",
                            command=self.fechar_aplicacao,
                            bg='#e74c3c', fg='white',
                            font=('Arial', 14, 'bold'),
                            width=15, height=2,
                            cursor='hand2')
        btn_sair.grid(row=0, column=1, padx=15)
        
        # Info de teste
        info_frame = tk.Frame(self.root, bg='#34495e')
        info_frame.pack(pady=(30, 0))
        
        tk.Label(info_frame, text="Usuários de teste:",
                font=('Arial', 10, 'bold'),
                bg='#34495e', fg='#ecf0f1').pack()
        
        tk.Label(info_frame, text="Admin: admin / admin123",
                font=('Arial', 9),
                bg='#34495e', fg='#95a5a6').pack()
        
        tk.Label(info_frame, text="Cliente: cliente / 123",
                font=('Arial', 9),
                bg='#34495e', fg='#95a5a6').pack()
        
        tk.Label(info_frame, text="Estúdio: estudio / 123",
                font=('Arial', 9),
                bg='#34495e', fg='#95a5a6').pack()
        
        # Binds
        self.entry_senha.bind('<Return>', lambda event: self.fazer_login())
        self.entry_login.bind('<Return>', lambda event: self.entry_senha.focus())
        self.entry_login.focus()
    
    def fazer_login(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha!", parent=self.root)
            return
        
        try:
            usuario = self.validar_credenciais(login, senha)
            
            if usuario:
                perfil = usuario['nome_perfil'].lower()
                
                # SOLUÇÃO: Esconder a janela principal antes de abrir o perfil
                self.root.withdraw()
                
                # Abrir janela do perfil correto
                if perfil == 'admin':
                    janela_perfil = AppAdmin(self.root)
                elif perfil == 'estúdio':
                    janela_perfil = AppEstudio(self.root)
                else:  # cliente
                    janela_perfil = AppCliente(self.root)
                
                # SOLUÇÃO: Configurar retorno ao login quando perfil fechar
                def ao_fechar_perfil():
                    janela_perfil.janela.destroy()
                    self.limpar_campos()
                    self.root.deiconify()  # Mostrar login novamente
                
                janela_perfil.janela.protocol("WM_DELETE_WINDOW", ao_fechar_perfil)
                
            else:
                messagebox.showerror("Erro", "Login ou senha incorretos!", parent=self.root)
                self.limpar_campos()
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}", parent=self.root)
            print(f"Erro detalhado: {e}")
    
    def validar_credenciais(self, login, senha):
        try:
            # Hash da senha para comparação
            senha_hash = hashlib.md5(senha.encode()).hexdigest()
            
            query = """
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, 
                       p.nome_perfil, c.id_perfil
                FROM cliente c
                INNER JOIN perfil p ON c.id_perfil = p.id_perfil
                WHERE c.login = %s AND c.senha = %s
            """
            self.dao.cursor.execute(query, (login, senha_hash))
            resultado = self.dao.cursor.fetchone()
            
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
            raise e
    
    def limpar_campos(self):
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_login.focus()
    
    def fechar_aplicacao(self):
        try:
            if self.dao.connection:
                self.dao.connection.close()
        except:
            pass
        self.root.quit()
        self.root.destroy()
    
    def iniciar(self):
        self.root.mainloop()
