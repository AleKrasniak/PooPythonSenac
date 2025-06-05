# app_admin.py
import tkinter as tk
from tkinter import messagebox, ttk
from clienteDAO import ClienteDAO
from cliente import Cliente
from administrador import Administrador


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
            ("Login:", "entry_login"),
            ("Senha:", "entry_senha")  # CAMPO DE SENHA ADICIONADO
        ]
        
        for label_text, attr_name in campos:
            tk.Label(frame_campos, text=label_text, bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
            
            # Para o campo senha, usar show='*' para ocultar texto
            if attr_name == "entry_senha":
                entry = tk.Entry(frame_campos, width=40, show='*')
            else:
                entry = tk.Entry(frame_campos, width=40)
                
            entry.grid(row=row, column=1, pady=2, padx=(10,0))
            setattr(self, attr_name, entry)
            row += 1

        # Endereço
        tk.Label(frame_campos, text="Endereço:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
        self.combo_endereco = ttk.Combobox(frame_campos, width=37, state='readonly')
        self.combo_endereco['values'] = [f"{id_end} - {endereco}" for id_end, endereco in self.enderecos]
        self.combo_endereco.grid(row=row, column=1, pady=2, padx=(10,0))
        row += 1
        
        # Perfil
        tk.Label(frame_campos, text="Perfil:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=2)
        self.combo_perfil = ttk.Combobox(frame_campos, width=37, state='readonly')
        self.combo_perfil['values'] = ["1 - Cliente", "2 - Estúdio", "3 - Admin"]
        self.combo_perfil.grid(row=row, column=1, pady=2, padx=(10,0))
        
        # Pré-selecionar Admin para facilitar criação de usuários admin
        self.combo_perfil.set("3 - Admin")
        
        # BOTÕES
        frame_botoes = tk.Frame(self.root, bg='#f0f0f0')
        frame_botoes.pack(pady=20)
        
        # Primeira linha de botões
        frame_botoes1 = tk.Frame(frame_botoes, bg='#f0f0f0')
        frame_botoes1.pack(pady=5)
        
        botoes1 = [
            ("CRIAR USUÁRIO", self.criar_cliente, '#27ae60'),
            ("LISTAR TODOS", self.listar_clientes, '#3498db'),
            ("BUSCAR POR ID", self.buscar_por_id, '#f39c12'),
            ("ATUALIZAR", self.atualizar_cliente, '#e67e22')
        ]
        
        for texto, comando, cor in botoes1:
            btn = tk.Button(frame_botoes1, text=texto, command=comando,
                           bg=cor, fg='white', font=('Arial', 10, 'bold'),
                           width=15, height=2, cursor='hand2')
            btn.pack(side='left', padx=5)
        
        # Segunda linha de botões
        frame_botoes2 = tk.Frame(frame_botoes, bg='#f0f0f0')
        frame_botoes2.pack(pady=5)
        
        botoes2 = [
            ("DELETAR", self.deletar_cliente, '#e74c3c'),
            ("LIMPAR CAMPOS", self.limpar_campos, '#95a5a6'),
            ("CRIAR ADMIN PADRÃO", self.criar_admin_padrao, '#8e44ad')
        ]
        
        for texto, comando, cor in botoes2:
            btn = tk.Button(frame_botoes2, text=texto, command=comando,
                           bg=cor, fg='white', font=('Arial', 10, 'bold'),
                           width=15, height=2, cursor='hand2')
            btn.pack(side='left', padx=5)
        
        # Área de resultados
        frame_resultados = tk.Frame(self.root, bg='#f0f0f0')
        frame_resultados.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(frame_resultados, text="RESULTADOS:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(anchor='w')
        
        # Scrollbar para o texto
        frame_text = tk.Frame(frame_resultados)
        frame_text.pack(fill='both', expand=True)
        
        self.text_resultados = tk.Text(frame_text, height=12, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(frame_text, orient="vertical", command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar.set)
        
        self.text_resultados.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def criar_admin_padrao(self):
        """Cria o usuário admin padrão com login 'adminale' e senha '123'"""
        try:
            # Limpar campos
            self.limpar_campos()
            
            # Definir dados do admin padrão
            admin_data = {
                'nome': 'Administrador Geral',
                'email': 'admin@busquestudios.com',
                'cpf': '000.000.000-00',
                'telefone': '(41) 99999-9999',
                'dt_nasc': '1990-01-01',
                'login': 'admale',
                'senha': '123'
            }
            
            # Preencher campos
            self.entry_nome.insert(0, admin_data['nome'])
            self.entry_email.insert(0, admin_data['email'])
            self.entry_cpf.insert(0, admin_data['cpf'])
            self.entry_telefone.insert(0, admin_data['telefone'])
            self.entry_dt_nasc.insert(0, admin_data['dt_nasc'])
            self.entry_login.insert(0, admin_data['login'])
            self.entry_senha.insert(0, admin_data['senha'])
            
            # Selecionar perfil Admin
            self.combo_perfil.set("3 - Admin")
            
            # Selecionar primeiro endereço se disponível
            if self.enderecos:
                self.combo_endereco.set(f"{self.enderecos[0][0]} - {self.enderecos[0][1]}")
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', 
                "✅ DADOS DO ADMIN PADRÃO PREENCHIDOS:\n"
                f"Login: {admin_data['login']}\n"
                f"Senha: {admin_data['senha']}\n"
                f"Nome: {admin_data['nome']}\n\n"
                "👆 Clique em 'CRIAR USUÁRIO' para salvar no banco de dados."
            )
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao preencher dados do admin: {str(e)}")

    def criar_cliente(self):
        """Cria um novo cliente/usuário"""
        try:
            # Validar campos obrigatórios
            nome = self.entry_nome.get().strip()
            email = self.entry_email.get().strip()
            cpf = self.entry_cpf.get().strip()
            telefone = self.entry_telefone.get().strip()
            login = self.entry_login.get().strip()
            senha = self.entry_senha.get().strip()
            
            if not all([nome, email, cpf, telefone]):
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (*)")
                return
            
            # Obter dados opcionais
            dt_nasc = self.entry_dt_nasc.get().strip() or None
            
            # Obter endereço selecionado
            endereco_sel = self.combo_endereco.get()
            id_endereco = int(endereco_sel.split(' - ')[0]) if endereco_sel else self.enderecos[0][0]
            
            # Obter perfil selecionado
            perfil_sel = self.combo_perfil.get()
            id_perfil = int(perfil_sel.split(' - ')[0]) if perfil_sel else 1
            
            # Criar cliente
            cliente = Cliente(
                nome=nome,
                email=email,
                telefone=telefone,
                cpf=cpf,
                dt_nasc=dt_nasc,
                id_endereco=id_endereco,
                id_perfil=id_perfil,
                login=login,
                senha=senha
            )
            
            resultado = self.dao.criar(cliente)
            
            if "sucesso" in resultado.lower():
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', f"✅ {resultado}")
                self.limpar_campos()
            else:
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', f"❌ {resultado}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar usuário: {str(e)}")

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        campos = [self.entry_id_cliente, self.entry_nome, self.entry_email, 
                 self.entry_cpf, self.entry_telefone, self.entry_dt_nasc, 
                 self.entry_login, self.entry_senha]
        
        for campo in campos:
            campo.delete(0, tk.END)
        
        self.combo_endereco.set('')
        self.combo_perfil.set('')

    def listar_clientes(self):
        """Lista todos os clientes"""
        try:
            resultado = self.dao.listar()
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar: {str(e)}")

    def buscar_por_id(self):
        """Busca cliente por ID"""
        try:
            id_cliente = self.entry_id_cliente.get().strip()
            if not id_cliente:
                messagebox.showwarning("Atenção", "Informe o ID do cliente")
                return
            
            resultado = self.dao.buscar_por_id(int(id_cliente))
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {str(e)}")

    def atualizar_cliente(self):
        """Atualiza cliente existente"""
        try:
            id_cliente = self.entry_id_cliente.get().strip()
            if not id_cliente:
                messagebox.showwarning("Atenção", "Informe o ID do cliente para atualizar")
                return
            
            # Validar campos obrigatórios
            nome = self.entry_nome.get().strip()
            email = self.entry_email.get().strip()
            cpf = self.entry_cpf.get().strip()
            telefone = self.entry_telefone.get().strip()
            
            if not all([nome, email, cpf, telefone]):
                messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (*)")
                return
            
            # Obter dados
            dt_nasc = self.entry_dt_nasc.get().strip() or None
            login = self.entry_login.get().strip()
            senha = self.entry_senha.get().strip()
            
            endereco_sel = self.combo_endereco.get()
            id_endereco = int(endereco_sel.split(' - ')[0]) if endereco_sel else None
            
            perfil_sel = self.combo_perfil.get()
            id_perfil = int(perfil_sel.split(' - ')[0]) if perfil_sel else None
            
            # Criar cliente com ID
            cliente = Cliente(
                nome=nome,
                email=email,
                telefone=telefone,
                cpf=cpf,
                dt_nasc=dt_nasc,
                id_endereco=id_endereco,
                id_perfil=id_perfil,
                login=login,
                senha=senha
            )
            cliente.id_cliente = int(id_cliente)
            
            resultado = self.dao.atualizar(cliente)
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")

    def deletar_cliente(self):
        """Deleta cliente por ID"""
        try:
            id_cliente = self.entry_id_cliente.get().strip()
            if not id_cliente:
                messagebox.showwarning("Atenção", "Informe o ID do cliente para deletar")
                return
            
            # Confirmação
            resposta = messagebox.askyesno("Confirmar", 
                                         f"Tem certeza que deseja deletar o cliente ID {id_cliente}?")
            if resposta:
                resultado = self.dao.deletar(int(id_cliente))
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', resultado)
                self.limpar_campos()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar: {str(e)}")