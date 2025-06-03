# app_admin.py
import tkinter as tk
from tkinter import messagebox, ttk
from clienteDAO import ClienteDAO
from cliente import Cliente

class AppAdmin:
    def __init__(self, root):
        self.dao = ClienteDAO()
        self.root = root
        self.perfil_id = 3  # PERFIL FIXO: Admin
        self.perfil_nome = "Admin"
        self.modo_admin = True  # MODO ADMIN ATIVADO
        
        self.root.title("Área Administrativa - BusqueStudios")
        self.root.geometry("800x800")
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
        titulo = tk.Label(self.root, text="ÁREA ADMINISTRATIVA", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        titulo.pack(pady=10)
        
        # INDICADOR DO PERFIL ADMIN
        frame_perfil = tk.Frame(self.root, bg='#f5f5f5', relief='ridge', bd=2)
        frame_perfil.pack(pady=5, padx=20, fill='x')
        
        tk.Label(frame_perfil, 
                text=f"🔐 MODO ADMINISTRADOR ATIVO", 
                font=('Arial', 12, 'bold'), 
                bg='#f5f5f5', 
                fg='#95a5a6').pack(pady=5)
        
        tk.Label(frame_perfil, 
                text="Você pode criar, listar, atualizar e deletar qualquer registro.", 
                font=('Arial', 9, 'italic'), 
                bg='#f5f5f5', 
                fg='#666').pack(pady=(0,5))
        
        # Frame para campos do formulário
        frame_campos = tk.Frame(self.root, bg='#f0f0f0')
        frame_campos.pack(pady=10, padx=20, fill='x')
        
        row = 0
        
        # ID Cliente (para atualizar/deletar)
        tk.Label(frame_campos, text="ID Cliente (para atualizar/deletar):", 
                bg='#f0f0f0', font=('Arial', 9)).grid(row=row, column=0, sticky='w', pady=2)
        self.entry_id_cliente = tk.Entry(frame_campos, width=40)
        self.entry_id_cliente.grid(row=row, column=1, pady=2, padx=(10,0))
        row += 1
        
        # Campos do formulário
        campos = [
            ("Nome *:", "entry_nome"),
            ("Email *:", "entry_email"),
            ("CPF/CNPJ *:", "entry_cpf"),
            ("Telefone *:", "entry_telefone"),
            ("Data Nasc/Fund (YYYY-MM-DD):", "entry_dt_nasc"),
            ("Login:", "entry_login")
        ]
        
        for label_text, attr_name in campos:
            tk.Label(frame_campos, text=label_text, bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
            entry = tk.Entry(frame_campos, width=40)
            entry.grid(row=row, column=1, pady=2, padx=(10,0))
            setattr(self, attr_name, entry)
            row += 1
