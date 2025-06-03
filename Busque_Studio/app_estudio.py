# app_estudio.py
import tkinter as tk
from tkinter import messagebox, ttk
from clienteDAO import ClienteDAO
from cliente import Cliente

class AppEstudio:
    def __init__(self, root):
        self.dao = ClienteDAO()
        self.root = root
        self.perfil_id = 2  # PERFIL FIXO: Estúdio
        self.perfil_nome = "Estúdio"
        
        self.root.title("Cadastro de Estúdio - BusqueStudios")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Carrega endereços disponíveis
        self.enderecos = self.carregar_enderecos()
        
        self.criar_interface()
        
    def carregar_enderecos(self):
        """Carrega endereços disponíveis do banco de dados"""
        try:
            cursor = self.dao.cursor
            cursor.execute("""SELECT id_endereco, 
                               CONCAT(rua, ', ', numero, ' - ', bairro) as endereco_completo 
                               FROM endereco""")
            return cursor.fetchall()
        except:
            # Dados de exemplo se não conseguir carregar do banco
            return [(1, 'Rua A, 123 - Centro'), (2, 'Av. B, 456 - Jardim')]
        
    def criar_interface(self):
        # TÍTULO
        titulo = tk.Label(self.root, text="CADASTRO DE ESTÚDIO", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        titulo.pack(pady=10)
        
        # INDICADOR DO PERFIL (FIXO)
        frame_perfil = tk.Frame(self.root, bg='#fde8e8', relief='ridge', bd=2)
        frame_perfil.pack(pady=5, padx=20, fill='x')
        
        tk.Label(frame_perfil, 
                text=f"✓ PERFIL: {self.perfil_nome} (ID: {self.perfil_id})", 
                font=('Arial', 12, 'bold'), 
                bg='#fde8e8', 
                fg='#e74c3c').pack(pady=5)
        
        tk.Label(frame_perfil, 
                text="Você será cadastrado automaticamente como Estúdio.", 
                font=('Arial', 9, 'italic'), 
                bg='#fde8e8', 
                fg='#666').pack(pady=(0,5))
        
        # Frame para campos do formulário
        frame_campos = tk.Frame(self.root, bg='#f0f0f0')
        frame_campos.pack(pady=10, padx=20, fill='x')
        
        row = 0
        
        # Campos específicos para estúdio (você pode personalizar)
        campos = [
            ("Nome do Estúdio *:", "entry_nome"),
            ("Email *:", "entry_email"),
            ("CNPJ *:", "entry_cpf"),  # Usando campo CPF para CNPJ
            ("Telefone *:", "entry_telefone"),
            ("Data de Fundação (YYYY-MM-DD):", "entry_dt_nasc"),
            ("Login:", "entry_login")
        ]
        
        for label_text, attr_name in campos:
            tk.Label(frame_campos, text=label_text, bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
            entry = tk.Entry(frame_campos, width=40)
            entry.grid(row=row, column=1, pady=2, padx=(10,0))
            setattr(self, attr_name, entry)
            row += 1
        
        # Campo senha (com show='*')
        tk.Label(frame_campos, text="Senha:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
        self.entry_senha = tk.Entry(frame_campos, width=40, show='*')
        self.entry_senha.grid(row=row, column=1, pady=2, padx=(10,0))
        row += 1
        
        # Tipo de estúdio (substituindo gênero)
        tk.Label(frame_campos, text="Tipo de Estúdio:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
        self.combo_genero = ttk.Combobox(frame_campos, values=['Fotografia', 'Tatuagem', 'Design', 'Audio', 'Vídeo'], width=37, state='readonly')
        self.combo_genero.grid(row=row, column=1, pady=2, padx=(10,0))
        row += 1
        
        # Combo Endereço
        tk.Label(frame_campos, text="Endereço:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
        endereco_valores = [f"{e[1]}" for e in self.enderecos]
        self.combo_endereco = ttk.Combobox(frame_campos, values=endereco_valores, width=37, state='readonly')
        self.combo_endereco.grid(row=row, column=1, pady=2, padx=(10,0))
        
        # Botões
        self.criar_botoes()
        
    def criar_botoes(self):
        """Cria botões para usuário comum"""
        frame_botoes = tk.Frame(self.root, bg='#f0f0f0')
        frame_botoes.pack(pady=20)
        
        # Botão principal - Cadastrar
        btn_cadastrar = tk.Button(frame_botoes, 
                                 text="CADASTRAR-SE COMO ESTÚDIO", 
                                 command=self.criar,
                                 bg='#e74c3c', fg='white', 
                                 font=('Arial', 12, 'bold'),
                                 width=25, height=3)
        btn_cadastrar.grid(row=0, column=0, padx=5)
        
        # Botão limpar
        btn_limpar = tk.Button(frame_botoes, text="LIMPAR CAMPOS", command=self.limpar_campos,
                              bg='#607D8B', fg='white', font=('Arial', 10, 'bold'),
                              width=15, height=2)
        btn_limpar.grid(row=1, column=0, pady=10)
    
    def get_id_endereco_selecionado(self):
        """Retorna o ID do endereço selecionado"""
        endereco_descricao = self.combo_endereco.get()
        if not endereco_descricao:
            return None
        
        for id_endereco, descricao in self.enderecos:
            if descricao == endereco_descricao:
                return id_endereco
        return None
    
    def criar(self):
        """Cria novo estúdio com PERFIL PRÉ-DEFINIDO"""
        try:
            # Validação de campos obrigatórios
            if not all([self.entry_nome.get(), self.entry_email.get(), 
                       self.entry_cpf.get(), self.entry_telefone.get()]):
                messagebox.showwarning("Erro", "Preencha os campos obrigatórios (*)!")
                return
            
            # Cria objeto Cliente com PERFIL FIXO = Estúdio
            cliente = Cliente(
                id_perfil=self.perfil_id,  # PERFIL FIXO = 2 (Estúdio)
                id_endereco=self.get_id_endereco_selecionado(),
                nome=self.entry_nome.get(),
                dt_nasc=self.entry_dt_nasc.get() if self.entry_dt_nasc.get() else None,
                genero=self.combo_genero.get() if self.combo_genero.get() else None,
                telefone=self.entry_telefone.get(),
                cpf=self.entry_cpf.get(),  # Será CNPJ para estúdios
                email=self.entry_email.get(),
                login=self.entry_login.get() if self.entry_login.get() else None,
                senha=self.entry_senha.get() if self.entry_senha.get() else None
            )
            
            self.dao.criar(cliente)
            messagebox.showinfo("SUCESSO!", 
                               f"Cadastro realizado com sucesso!\n\n"
                               f"Você foi cadastrado como: {self.perfil_nome}\n"
                               f"Perfil ID: {self.perfil_id}")
                
            self.limpar_campos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar estúdio: {str(e)}")
    
    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        campos = [
            self.entry_nome, self.entry_email, self.entry_cpf, 
            self.entry_telefone, self.entry_dt_nasc, self.entry_login, self.entry_senha
        ]
        
        for campo in campos:
            campo.delete(0, tk.END)
        
        self.combo_genero.set('')
        self.combo_endereco.set('')