import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector
from clienteDAO import ClienteDAO
from estudioDAO import EstudioDAO
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

class AppPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BusqueStudios - Sistema Principal")
        
        # Configuração de tamanho fixo mais adequado
        self.root.geometry("800x1000")
        self.root.state('zoomed')  # Windows
        
        # Centraliza a janela
        self.centralizar_janela()
        
        # Configuração de cor de fundo
        self.root.configure(bg='#2c3e50')
        
        # Tamanho mínimo
        self.root.minsize(700, 600)  # Reduzido para melhor compatibilidade
        
        self.dao = ClienteDAO()
        self.estudio_dao = EstudioDAO()
        self.usuario_logado = None
        
        self.criar_interface()
        
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 800
        height = 1000
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def criar_interface_scroll(self):
        """Cria interface com scroll para telas pequenas"""
        # Limpa widgets existentes
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Container principal com scroll
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg='#2c3e50', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2c3e50')
        
        # Configuração do scroll
        def atualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", atualizar_scroll)
        
        # Cria janela no canvas e configura scroll
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Centraliza horizontalmente o conteúdo
        def centralizar_horizontal(event):
            # Atualiza a largura do scrollable_frame para preencher o canvas
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', centralizar_horizontal)
        
        # Pack do canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll com mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Container centralizado para o conteúdo
        content_container = tk.Frame(scrollable_frame, bg='#2c3e50')
        content_container.pack(expand=True, fill='both')
        
        # Frame centralizado para todo o conteúdo
        center_frame = tk.Frame(content_container, bg='#2c3e50')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Cabeçalho
        self.criar_cabecalho(center_frame)
        
        # Seção de Login
        self.criar_secao_login(center_frame)
        
        # Separador
        separator = tk.Frame(center_frame, height=2, bg='#34495e', width=500)
        separator.pack(pady=10)
        separator.pack_propagate(False)
        
        # Seção de Cadastro
        self.criar_secao_cadastro(center_frame)
        
        # Espaço extra no final
        tk.Frame(center_frame, height=50, bg='#2c3e50').pack()
        
        # Garante altura mínima para centralização
        content_container.configure(height=800)
        
        return canvas, scrollable_frame
    
    def criar_interface(self):
        """Cria toda a interface gráfica principal"""
        # Verifica se a tela é pequena
        screen_height = self.root.winfo_screenheight()
        
        if screen_height < 800:  # Se a tela for menor que 800px
            self.criar_interface_scroll()
        else:
            self.criar_interface_normal()
    
    def criar_interface_normal(self):
        """Cria interface normal sem scroll"""
        # Limpa widgets existentes
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Container principal centralizado
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True)
        
        # Frame centralizado para todo o conteúdo
        center_frame = tk.Frame(main_container, bg='#2c3e50')
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Cabeçalho
        self.criar_cabecalho(center_frame)
        
        # Seção de Login
        self.criar_secao_login(center_frame)
        
        # Separador
        separator = tk.Frame(center_frame, height=2, bg='#34495e', width=500)
        separator.pack(pady=10)
        separator.pack_propagate(False)
        
        # Seção de Cadastro
        self.criar_secao_cadastro(center_frame)
    
    def criar_cabecalho(self, parent):
        """Cria o cabeçalho da aplicação"""
        header_frame = tk.Frame(parent, bg='#2c3e50')
        header_frame.pack(pady=(0, 15))
        
        title_label = tk.Label(header_frame, text="BUSQUE STUDIOS", 
                font=('Arial', 26, 'bold'), 
                bg='#2c3e50', fg='white')
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Sistema de Gestão", 
                font=('Arial', 12), 
                bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack(pady=(3, 0))
        
    def criar_secao_login(self, parent):
        """Cria a seção de login com campos e botão"""
        # Frame de login
        frame_login = tk.Frame(parent, bg='#34495e', relief='ridge', bd=2)
        frame_login.pack(pady=10)
        
        # Título do login
        login_title = tk.Label(frame_login, text="FAZER LOGIN", 
                font=('Arial', 15, 'bold'), 
                bg='#34495e', fg='white')
        login_title.pack(pady=12)
        
        # Frame para campos
        frame_campos = tk.Frame(frame_login, bg='#34495e')
        frame_campos.pack(pady=10, padx=30)
        
        # Campo de Login
        tk.Label(frame_campos, text="Login:", 
                font=('Arial', 11, 'bold'), bg='#34495e', fg='white').pack(anchor='w', pady=(0, 3))
        self.entry_login = tk.Entry(frame_campos, font=('Arial', 11), relief='flat', bd=5, width=35)
        self.entry_login.pack(pady=(0, 10))
        
        # Campo de Senha
        tk.Label(frame_campos, text="Senha:", 
                font=('Arial', 11, 'bold'), bg='#34495e', fg='white').pack(anchor='w', pady=(0, 3))
        self.entry_senha = tk.Entry(frame_campos, font=('Arial', 11), show='*', relief='flat', bd=5, width=35)
        self.entry_senha.pack(pady=(0, 12))
        
        # Botão de Login
        btn_login = tk.Button(frame_campos, text="ENTRAR", 
                 command=self.fazer_login,
                 bg='#27ae60', fg='white',
                 font=('Arial', 12, 'bold'),
                 height=2, width=15,
                 cursor='hand2',
                 relief='flat',
                 bd=0,
                 activebackground='#229954',
                 activeforeground='white')
        btn_login.pack(pady=(0, 15))
        
        # Efeito de hover
        self.add_hover_effect(btn_login, '#27ae60', '#229954')
        
        # Bind Enter para login
        self.entry_senha.bind('<Return>', lambda event: self.fazer_login())
        
    def criar_secao_cadastro(self, parent):
        """Cria a seção de cadastro com botões"""
        # Frame de cadastro
        cadastro_frame = tk.Frame(parent, bg='#2c3e50')
        cadastro_frame.pack(pady=10)
        
        # Título
        tk.Label(cadastro_frame, text="OU CADASTRE-SE", 
                font=('Arial', 16, 'bold'), 
                bg='#2c3e50', fg='#bdc3c7').pack(pady=(0, 15))
        
        # Frame para botões de cadastro
        frame_botoes_cadastro = tk.Frame(cadastro_frame, bg='#2c3e50')
        frame_botoes_cadastro.pack(pady=5)
        
        # Botão Cadastrar Cliente
        btn_cliente = tk.Button(frame_botoes_cadastro, 
                 text="CADASTRAR\nCLIENTE",
                 command=self.abrir_cadastro_cliente,
                 bg='#BA4467', fg='white',
                 font=('Arial', 11, 'bold'),
                 height=3, width=16,
                 cursor='hand2',
                 relief='flat',
                 bd=0,
                 activebackground='#A53A5A',
                 activeforeground='white')
        btn_cliente.pack(side='left', padx=10)
        self.add_hover_effect(btn_cliente, '#BA4467', '#A53A5A')
        
        # Botão Cadastrar Estúdio
        btn_estudio = tk.Button(frame_botoes_cadastro, 
                 text="CADASTRAR\nESTÚDIO",
                 command=self.abrir_cadastro_estudio,
                 bg='#e74c3c', fg='white',
                 font=('Arial', 11, 'bold'),
                 height=3, width=16,
                 cursor='hand2',
                 relief='flat',
                 bd=0,
                 activebackground='#C0392B',
                 activeforeground='white')
        btn_estudio.pack(side='left', padx=10)
        self.add_hover_effect(btn_estudio, '#e74c3c', '#C0392B')
        
        # Botão Admin
        btn_admin = tk.Button(cadastro_frame, 
                 text="ÁREA ADMINISTRATIVA",
                 command=self.abrir_area_admin,
                 bg='#95a5a6', fg='white',
                 font=('Arial', 10, 'bold'),
                 height=2, width=22,
                 cursor='hand2',
                 relief='flat',
                 bd=0,
                 activebackground='#7F8C8D',
                 activeforeground='white')
        btn_admin.pack(pady=(20, 10))
        self.add_hover_effect(btn_admin, '#95a5a6', '#7F8C8D')
    
    def add_hover_effect(self, button, normal_color, hover_color):
        """Adiciona efeito de hover aos botões"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def fazer_login(self):
        """Realiza o login do usuário"""
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        
        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha!")
            return
            
        try:
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
        """Valida as credenciais no banco de dados"""
        try:
            cursor = self.dao.cursor
            
            # Verifica em administradores
            query_admin = """SELECT a.id_administrador as id, a.nome, a.email, 
                           '' as telefone, '' as cpf, p.nome as nome_perfil, 
                           a.id_perfil, 'administrador' as tipo_usuario
                           FROM administrador a
                           INNER JOIN perfil p ON a.id_perfil = p.id_perfil
                           WHERE a.login = %s AND a.senha = %s"""
            cursor.execute(query_admin, (login, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                return self.formatar_usuario(resultado)
            
            # Verifica em clientes
            query_cliente = """SELECT c.id_cliente as id, c.nome, c.email, 
                             c.telefone, c.cpf, p.nome as nome_perfil, 
                             c.id_perfil, 'cliente' as tipo_usuario
                             FROM cliente c
                             INNER JOIN perfil p ON c.id_perfil = p.id_perfil
                             WHERE c.login = %s AND c.senha = %s"""
            cursor.execute(query_cliente, (login, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                return self.formatar_usuario(resultado)
            
            # Verifica em estúdios
            query_estudio = """SELECT e.id_estudio as id, e.nome_estudio as nome, 
                             e.email, e.telefone, e.cnpj as cpf, 
                             p.nome as nome_perfil, e.id_perfil, 
                             'estudio' as tipo_usuario
                             FROM estudio e
                             INNER JOIN perfil p ON e.id_perfil = p.id_perfil
                             WHERE e.login = %s AND e.senha = %s"""
            cursor.execute(query_estudio, (login, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                return self.formatar_usuario(resultado)
            
            return None
            
        except Exception as e:
            print(f"Erro na validação: {e}")
            return None
    
    def formatar_usuario(self, resultado):
        """Formata os dados do usuário para um dicionário"""
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
    
    def mostrar_area_logado(self):
        """Mostra a área específica do usuário logado com scroll se necessário"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Mantém configuração da janela
        self.root.state('zoomed')
        
        # Verifica se precisa de scroll
        screen_height = self.root.winfo_screenheight()
        
        if screen_height < 800:
            self.mostrar_area_logado_scroll()
        else:
            self.mostrar_area_logado_normal()
    
    def mostrar_area_logado_scroll(self):
        """Área logado com scroll"""
        # Container principal com scroll
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        # Configuração do scroll
        def atualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", atualizar_scroll)
        
        # Cria janela no canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Centraliza horizontalmente o conteúdo
        def centralizar_horizontal(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        canvas.bind('<Configure>', centralizar_horizontal)
        
        # Pack do canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll com mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Header
        frame_header = tk.Frame(scrollable_frame, bg='#27ae60', height=120)
        frame_header.pack(fill='x')
        frame_header.pack_propagate(False)
        
        welcome_label = tk.Label(frame_header, text=f"Bem-vindo(a), {self.usuario_logado['nome']}!", 
                font=('Arial', 20, 'bold'), 
                bg='#27ae60', fg='white')
        welcome_label.pack(pady=(20, 5))
        
        profile_label = tk.Label(frame_header, text=f"Perfil: {self.usuario_logado['nome_perfil']}", 
                font=('Arial', 14), 
                bg='#27ae60', fg='white')
        profile_label.pack(pady=(0, 20))
        
        # Container para centralizar o conteúdo principal
        content_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        content_container.pack(fill='both', expand=True)
        
        # Frame principal centralizado
        frame_main = tk.Frame(content_container, bg='#f0f0f0')
        frame_main.place(relx=0.5, rely=0.5, anchor='center')
        
        self.criar_opcoes_perfil(frame_main)
        
        # Botão de logout centralizado
        btn_logout = tk.Button(frame_main, text="SAIR", 
                 command=self.fazer_logout,
                 bg='#e74c3c', fg='white',
                 font=('Arial', 12, 'bold'),
                 height=2, width=15,
                 cursor='hand2',
                 relief='flat',
                 bd=0,
                 activebackground='#C0392B',
                 activeforeground='white')
        btn_logout.pack(pady=40)
        self.add_hover_effect(btn_logout, '#e74c3c', '#C0392B')
        
        # Garante altura mínima para centralização
        content_container.configure(height=600)
    
    def mostrar_area_logado_normal(self):
        """Área logado normal"""
        # Container principal
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True)
        
        # Header
        frame_header = tk.Frame(main_container, bg='#27ae60', height=120)
        frame_header.pack(fill='x')
        frame_header.pack_propagate(False)
        
        welcome_label = tk.Label(frame_header, text=f"Bem-vindo(a), {self.usuario_logado['nome']}!", 
                font=('Arial', 20, 'bold'), 
                bg='#27ae60', fg='white')
        welcome_label.pack(pady=(20, 5))
        
        profile_label = tk.Label(frame_header, text=f"Perfil: {self.usuario_logado['nome_perfil']}", 
                font=('Arial', 14), 
                bg='#27ae60', fg='white')
        profile_label.pack(pady=(0, 20))
        
        # Área principal
        frame_main = tk.Frame(main_container, bg='#f0f0f0')
        frame_main.pack(expand=True, pady=50)
        
        self.criar_opcoes_perfil(frame_main)
        
        # Botão de logout
        btn_logout = tk.Button(frame_main, text="SAIR", 
                 command=self.fazer_logout,
                 bg='#e74c3c', fg='white',
                 font=('Arial', 12, 'bold'),
                 height=2, width=15,
                 cursor='hand2',
                 relief='flat',
                 bd=0,
                 activebackground='#C0392B',
                 activeforeground='white')
        btn_logout.pack(pady=40)
        self.add_hover_effect(btn_logout, '#e74c3c', '#C0392B')
    
    def criar_opcoes_perfil(self, frame_parent):
        """Cria opções baseadas no tipo de usuário"""
        tipo_usuario = self.usuario_logado.get('tipo_usuario', 'cliente')
        
        if tipo_usuario == 'administrador':
            self.criar_opcoes_admin(frame_parent)
        elif tipo_usuario == 'cliente':
            self.criar_opcoes_cliente(frame_parent)
        elif tipo_usuario == 'estudio':
            self.criar_opcoes_estudio(frame_parent)
    
    def criar_opcoes_admin(self, frame_parent):
        """Opções para administradores"""
        tk.Label(frame_parent, text="ÁREA ADMINISTRATIVA", 
                font=('Arial', 22, 'bold'), 
                bg='#f0f0f0', fg='#95a5a6').pack(pady=30)
        
        botoes_info = [
            ("Gerenciar Usuários", self.gerenciar_usuarios, '#95a5a6', '#7F8C8D'),
            ("Aprovar Estúdios", self.aprovar_estudios, '#34495e', '#2C3E50'),
            ("Relatórios", self.gerar_relatorios, '#7f8c8d', '#6C7B7D')
        ]
        
        for texto, comando, cor, hover_cor in botoes_info:
            btn = tk.Button(frame_parent, text=texto, 
                     command=comando,
                     bg=cor, fg='white',
                     font=('Arial', 14, 'bold'),
                     width=25, height=2,
                     cursor='hand2',
                     relief='flat',
                     bd=0,
                     activebackground=hover_cor,
                     activeforeground='white')
            btn.pack(pady=15)
            self.add_hover_effect(btn, cor, hover_cor)
    
    def criar_opcoes_cliente(self, frame_parent):
        """Opções para clientes"""
        tk.Label(frame_parent, text="ÁREA DO CLIENTE", 
                font=('Arial', 22, 'bold'), 
                bg='#f0f0f0', fg='#BA4467').pack(pady=30)
        
        botoes_info = [
            ("Meu Perfil", self.abrir_meu_perfil, '#BA4467', '#A53A5A'),
            ("Buscar Estúdios", self.buscar_estudios, '#3498db', '#2980B9')
        ]
        
        for texto, comando, cor, hover_cor in botoes_info:
            btn = tk.Button(frame_parent, text=texto, 
                     command=comando,
                     bg=cor, fg='white',
                     font=('Arial', 14, 'bold'),
                     width=25, height=2,
                     cursor='hand2',
                     relief='flat',
                     bd=0,
                     activebackground=hover_cor,
                     activeforeground='white')
            btn.pack(pady=15)
            self.add_hover_effect(btn, cor, hover_cor)
    
    def criar_opcoes_estudio(self, frame_parent):
        """Opções para estúdios"""
        tk.Label(frame_parent, text="ÁREA DO ESTÚDIO", 
                font=('Arial', 22, 'bold'), 
                bg='#f0f0f0', fg='#e74c3c').pack(pady=30)
        
        botoes_info = [
            ("Meu Perfil", self.abrir_meu_perfil, '#e74c3c', '#C0392B'),
            ("Meus Serviços", self.gerenciar_servicos, '#f39c12', '#E67E22')
        ]
        
        for texto, comando, cor, hover_cor in botoes_info:
            btn = tk.Button(frame_parent, text=texto, 
                     command=comando,
                     bg=cor, fg='white',
                     font=('Arial', 14, 'bold'),
                     width=25, height=2,
                     cursor='hand2',
                     relief='flat',
                     bd=0,
                     activebackground=hover_cor,
                     activeforeground='white')
            btn.pack(pady=15)
            self.add_hover_effect(btn, cor, hover_cor)
    
    # Métodos das funcionalidades
    def gerenciar_usuarios(self):
        messagebox.showinfo("Admin", "Funcionalidade 'Gerenciar Usuários' em desenvolvimento!")

    def aprovar_estudios(self):
        messagebox.showinfo("Admin", "Funcionalidade 'Aprovar Estúdios' em desenvolvimento!")

    def gerar_relatorios(self):
        messagebox.showinfo("Admin", "Funcionalidade 'Relatórios' em desenvolvimento!")
        
    def abrir_meu_perfil(self):
        messagebox.showinfo("Perfil", "Funcionalidade 'Meu Perfil' em desenvolvimento!")
    
    def buscar_estudios(self):
        messagebox.showinfo("Busca", "Funcionalidade 'Buscar Estúdios' em desenvolvimento!")
    
    def gerenciar_servicos(self):
        messagebox.showinfo("Serviços", "Funcionalidade 'Meus Serviços' em desenvolvimento!")
    
    def abrir_cadastro_cliente(self):
        from app_cliente import AppCliente
        self.root.withdraw()
        janela_cliente = tk.Toplevel()
        AppCliente(janela_cliente)
        janela_cliente.protocol("WM_DELETE_WINDOW", lambda: self.fechar_janela_secundaria(janela_cliente))
        
    def abrir_cadastro_estudio(self):
        from app_estudio import AppEstudio
        self.root.withdraw()
        janela_estudio = tk.Toplevel()
        AppEstudio(janela_estudio)
        janela_estudio.protocol("WM_DELETE_WINDOW", lambda: self.fechar_janela_secundaria(janela_estudio))
        
    def abrir_area_admin(self):
        from app_admin import AppAdmin
        senha = simpledialog.askstring("Acesso Restrito", "Digite a senha de administrador:", show='*')
        
        if senha == "123":
            self.root.withdraw()
            janela_admin = tk.Toplevel()
            AppAdmin(janela_admin)
            janela_admin.protocol("WM_DELETE_WINDOW", lambda: self.fechar_janela_secundaria(janela_admin))
        else:
            messagebox.showerror("Erro", "Senha incorreta!")
    
    def fechar_janela_secundaria(self, janela):
        """Fecha janela secundária e volta para a principal"""
        janela.destroy()
        self.root.deiconify()
        self.root.state('zoomed')
    
    def fazer_logout(self):
        """Realiza logout do usuário"""
        self.usuario_logado = None
        self.criar_interface()
        messagebox.showinfo("Logout", "Logout realizado com sucesso!")
    
    def limpar_campos_login(self):
        """Limpa os campos de login"""
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
    
    def executar(self):
        """Inicia a aplicação"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AppPrincipal()
    app.executar()