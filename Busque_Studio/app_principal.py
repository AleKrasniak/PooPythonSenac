# app_principal.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from app_cliente import AppCliente
from app_estudio import AppEstudio
from app_admin import AppAdmin
import mysql.connector
from clienteDAO import ClienteDAO

class AppPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BusqueStudios - Sistema Principal")
        self.root.geometry("450x600")
        self.root.configure(bg='#2c3e50')
        
        self.dao = ClienteDAO()
        self.usuario_logado = None
        
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
        subtitulo.pack(pady=(0, 30))
        
        # SEÇÃO DE LOGIN
        self.criar_secao_login()
        
        # Separador
        separador = tk.Frame(self.root, height=2, bg='#34495e')
        separador.pack(fill='x', padx=40, pady=20)
        
        # SEÇÃO DE CADASTRO
        self.criar_secao_cadastro()
        
    def criar_secao_login(self):
        """Cria a seção de login"""
        # Frame de login
        frame_login = tk.Frame(self.root, bg='#34495e', relief='ridge', bd=2)
        frame_login.pack(pady=10, padx=40, fill='x')
        
        # Título da seção
        tk.Label(frame_login, text="FAZER LOGIN", 
                font=('Arial', 14, 'bold'), 
                bg='#34495e', fg='white').pack(pady=(10, 15))
        
        # Campos de login
        frame_campos = tk.Frame(frame_login, bg='#34495e')
        frame_campos.pack(pady=10, padx=20)
        
        # Login
        tk.Label(frame_campos, text="Login:", 
                font=('Arial', 10), bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        self.entry_login = tk.Entry(frame_campos, width=25, font=('Arial', 10))
        self.entry_login.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Senha
        tk.Label(frame_campos, text="Senha:", 
                font=('Arial', 10), bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=5)
        self.entry_senha = tk.Entry(frame_campos, width=25, font=('Arial', 10), show='*')
        self.entry_senha.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Botão de login
        btn_login = tk.Button(frame_login, text="ENTRAR", 
                             command=self.fazer_login,
                             bg='#27ae60', fg='white',
                             font=('Arial', 12, 'bold'),
                             width=15, height=2,
                             cursor='hand2')
        btn_login.pack(pady=15)
        
        # Bind Enter para fazer login
        self.entry_senha.bind('<Return>', lambda event: self.fazer_login())
        
    def criar_secao_cadastro(self):
        """Cria a seção de cadastros"""
        # Título da seção
        tk.Label(self.root, text="OU CADASTRE-SE", 
                font=('Arial', 14, 'bold'), 
                bg='#2c3e50', fg='#bdc3c7').pack(pady=(10, 20))
        
        # Frame para botões de cadastro
        frame_botoes = tk.Frame(self.root, bg='#2c3e50')
        frame_botoes.pack(expand=True)
        
        # Botão Cadastrar Cliente
        btn_cliente = tk.Button(frame_botoes, 
                               text="CADASTRAR CLIENTE",
                               command=self.abrir_cadastro_cliente,
                               bg='#BA4467', fg='white',
                               font=('Arial', 14, 'bold'),
                               width=20, height=2,
                               cursor='hand2')
        btn_cliente.pack(pady=10)
        
        # Botão Cadastrar Estúdio
        btn_estudio = tk.Button(frame_botoes, 
                               text="CADASTRAR ESTÚDIO",
                               command=self.abrir_cadastro_estudio,
                               bg='#e74c3c', fg='white',
                               font=('Arial', 14, 'bold'),
                               width=20, height=2,
                               cursor='hand2')
        btn_estudio.pack(pady=10)
        
        # Botão Admin
        btn_admin = tk.Button(frame_botoes, 
                             text="ÁREA ADMINISTRATIVA",
                             command=self.abrir_area_admin,
                             bg='#95a5a6', fg='white',
                             font=('Arial', 10),
                             width=20, height=1,
                             cursor='hand2')
        btn_admin.pack(pady=(30, 10))
        
    def fazer_login(self):
        """Realiza o login do usuário"""
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha!")
            return
            
        try:
            # Busca usuário no banco de dados
            usuario = self.validar_credenciais(login, senha)
            
            if usuario:
                self.usuario_logado = usuario
                self.mostrar_area_logado()
            else:
                messagebox.showerror("Erro", "Login ou senha incorretos!")
                self.limpar_campos_login()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")

    def validar_credenciais(self, login, senha):
        """Valida as credenciais do usuário no banco de dados"""
        try:
            cursor = self.dao.cursor
            
            # 1. PRIMEIRO: Buscar na tabela ADMINISTRADOR
            query_admin = """
                SELECT a.id_administrador as id, a.nome, a.email, 
                       '' as telefone, '' as cpf,
                       p.nome as nome_perfil, a.id_perfil,
                       'administrador' as tipo_usuario
                FROM administrador a
                INNER JOIN perfil p ON a.id_perfil = p.id_perfil
                WHERE a.login = %s AND a.senha = %s
            """
            
            cursor.execute(query_admin, (login, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'telefone': resultado[3],
                    'cpf': resultado[4],
                    'nome_perfil': resultado[5],
                    'id_perfil': resultado[6],
                    'tipo_usuario': resultado[7]
                }
            
            # 2. SE NÃO ACHOU ADMIN: Buscar na tabela CLIENTE
            query_cliente = """
                SELECT c.id_cliente as id, c.nome, c.email, c.telefone, c.cpf, 
                       p.nome as nome_perfil, c.id_perfil,
                       'cliente' as tipo_usuario
                FROM cliente c
                INNER JOIN perfil p ON c.id_perfil = p.id_perfil
                WHERE c.login = %s AND c.senha = %s
            """
            
            cursor.execute(query_cliente, (login, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'telefone': resultado[3],
                    'cpf': resultado[4],
                    'nome_perfil': resultado[5],
                    'id_perfil': resultado[6],
                    'tipo_usuario': resultado[7]
                }
            
            # 3. SE NÃO ACHOU NEM ADMIN NEM CLIENTE: Buscar na tabela ESTUDIO
            query_estudio = """
                SELECT e.id_estudio as id, e.nome_estudio as nome, e.email, 
                       e.telefone, e.cnpj as cpf,
                       p.nome as nome_perfil, e.id_perfil,
                       'estudio' as tipo_usuario
                FROM estudio e
                INNER JOIN perfil p ON e.id_perfil = p.id_perfil
                WHERE e.login = %s AND e.senha = %s
            """
            
            cursor.execute(query_estudio, (login, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'telefone': resultado[3],
                    'cpf': resultado[4],
                    'nome_perfil': resultado[5],
                    'id_perfil': resultado[6],
                    'tipo_usuario': resultado[7]
                }
            
            return None
            
        except Exception as e:
            print(f"Erro na validação: {e}")
            return None
    
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
        tipo_usuario = self.usuario_logado.get('tipo_usuario', 'cliente')
        
        # ADMINISTRADOR
        if tipo_usuario == 'administrador' or perfil_id == 1:  # Assumindo que perfil 1 é admin
            tk.Label(frame_parent, text="ÁREA ADMINISTRATIVA", 
                    font=('Arial', 18, 'bold'), 
                    bg='#f0f0f0', fg='#95a5a6').pack(pady=20)
            
            btn_usuarios = tk.Button(frame_parent, text="Gerenciar Usuários", 
                                   command=self.gerenciar_usuarios,
                                   bg='#95a5a6', fg='white',
                                   font=('Arial', 12, 'bold'),
                                   width=20, height=2)
            btn_usuarios.pack(pady=10)
            
            btn_estudios = tk.Button(frame_parent, text="Aprovar Estúdios", 
                                   command=self.aprovar_estudios,
                                   bg='#34495e', fg='white',
                                   font=('Arial', 12, 'bold'),
                                   width=20, height=2)
            btn_estudios.pack(pady=10)
            
            btn_relatorios = tk.Button(frame_parent, text="Relatórios", 
                                     command=self.gerar_relatorios,
                                     bg='#7f8c8d', fg='white',
                                     font=('Arial', 12, 'bold'),
                                     width=20, height=2)
            btn_relatorios.pack(pady=10)
        
        # CLIENTE
        elif tipo_usuario == 'cliente':
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
        
        # ESTÚDIO
        elif tipo_usuario == 'estudio':
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

    # Métodos para as funcionalidades do admin
    def gerenciar_usuarios(self):
        """Abre tela de gerenciamento de usuários"""
        messagebox.showinfo("Admin", "Funcionalidade 'Gerenciar Usuários' em desenvolvimento!")

    def aprovar_estudios(self):
        """Abre tela de aprovação de estúdios"""
        messagebox.showinfo("Admin", "Funcionalidade 'Aprovar Estúdios' em desenvolvimento!")

    def gerar_relatorios(self):
        """Abre tela de relatórios"""
        messagebox.showinfo("Admin", "Funcionalidade 'Relatórios' em desenvolvimento!")
        
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
        
        self.root.geometry("450x600")
        self.criar_interface()
        messagebox.showinfo("Logout", "Logout realizado com sucesso!")
    
    def limpar_campos_login(self):
        """Limpa os campos de login"""
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        
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
        
        if senha == "123":
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