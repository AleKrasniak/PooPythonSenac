import tkinter as tk
from tkinter import messagebox, ttk
from clienteDAO import ClienteDAO
from cliente import Cliente
from perfil import Perfil
from perfilDAO import perfilDAO
from administrador import Administrador
from enderecoDAO import EnderecoDAO  # ADICIONADOfrom endereco import Endereco
from endereco import Endereco


class AppAdmin:
    def __init__(self, root, callback_voltar=None):
        self.dao = ClienteDAO()
        self.endereco_dao = EnderecoDAO()  # ADICIONADO
        self.root = root
        self.callback_voltar = callback_voltar
        self.perfil_id = 3  # PERFIL FIXO: Admin
        self.perfil_nome = "Admin"
        self.modo_admin = True  # MODO ADMIN ATIVADO

        self.root.title("Área Administrativa - BusqueStudios")
        self.root.state('zoomed')  # Abre em tela cheia no Windows
        self.root.configure(bg='#f0f0f0')
    
        #label do CPF/CNPJ para poder alterar
        self.label_cpf_cnpj = None
    
        self.enderecos = self.carregar_enderecos()
        self.estados = self.carregar_estados() 
        self.estados_ibge = self.carregar_ufs()
    
        # Criar interface
        self.criar_interface()
    
        # Configurar o bind do combo_perfil APÓS a interface ser criada
        self.combo_perfil.bind('<<ComboboxSelected>>', self.on_perfil_change)

    def on_perfil_change(self, event=None):
        """Altera o label do campo CPF/CNPJ baseado no perfil selecionado"""
        perfil_sel = self.combo_perfil.get()
        if perfil_sel:
            id_perfil = int(perfil_sel.split(' - ')[0])
            
            # Encontrar o label CPF/CNPJ e alterá-lo
            if hasattr(self, 'label_cpf_cnpj') and self.label_cpf_cnpj:
                if id_perfil == 3:  # Estúdio
                    self.label_cpf_cnpj.config(text="CNPJ *:")
                else:  # Cliente ou Admin
                    self.label_cpf_cnpj.config(text="CPF *:")

    def carregar_enderecos(self):
        """Carrega endereços disponíveis do banco de dados"""
        cursor = self.dao.cursor
        cursor.execute("""SELECT id_endereco, 
                           CONCAT(rua, ', ', numero, ' - ', bairro) as endereco_completo 
                           FROM endereco""")
        return cursor.fetchall()

    def carregar_estados(self):
        """Carrega estados usando o EnderecoDAO"""

        return self.endereco_dao.listar_estados()
    
    def carregar_ufs(self):
        """Carrega estados da API do IBGE"""
        import requests
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        try:
            resposta = requests.get(url, timeout=5)
            resposta.raise_for_status()
            estados = resposta.json()
            estados.sort(key=lambda e: e['nome'])
            return estados
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar estados: {e}")
            return []

    def on_uf_selecionado(self, event):
        """Carrega cidades quando UF é selecionado"""
        import requests
        uf = self.combo_uf.get()
        estado = next((e for e in self.estados_ibge if e['sigla'] == uf), None)
        if not estado:
            self.combo_cidade['values'] = []
            self.combo_cidade.set('')
            return

        id_estado = estado['id']
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{id_estado}/municipios"
        try:
            resposta = requests.get(url, timeout=5)
            resposta.raise_for_status()
            cidades = [cidade['nome'] for cidade in resposta.json()]
            cidades.sort()
            self.combo_cidade['values'] = cidades
            self.combo_cidade.set('')
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar cidades: {e}")
            self.combo_cidade['values'] = []
            self.combo_cidade.set('')

    def criar_interface(self):
        # Container principal centralizado
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(expand=True, fill='both')

        # Canvas para permitir scroll
        canvas = tk.Canvas(main_container, bg='#f0f0f0', highlightthickness=0)
        
        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Frame scrollable que conterá todo o conteúdo
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        # Configurar scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Criar janela no canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame principal que será centralizado dentro do scrollable_frame
        content_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        content_frame.pack(expand=True, pady=30)  # Padding para centralização vertical

        # BOTÃO VOLTAR (se callback foi fornecido)
        if self.callback_voltar:
            self.criar_botao_voltar(content_frame)
        
        # TÍTULO
        titulo = tk.Label(content_frame, text="ÁREA ADMINISTRATIVA", 
                         font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#333')
        titulo.pack(pady=(0, 20))
        
        # INDICADOR DO PERFIL ADMIN
        frame_perfil = tk.Frame(content_frame, bg='#f5f5f5', relief='ridge', bd=2)
        frame_perfil.pack(pady=10, padx=20, fill='x')
        
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
        frame_campos = tk.Frame(content_frame, bg='#f0f0f0', relief='groove', bd=2)
        frame_campos.pack(pady=20, padx=40, fill='x')
        
        # Título dos campos
        tk.Label(frame_campos, text="FORMULÁRIO DE USUÁRIOS", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#333').pack(pady=(10, 15))
        
        # Container interno para os campos
        campos_container = tk.Frame(frame_campos, bg='#f0f0f0')
        campos_container.pack(padx=20, pady=10)
        
        row = 0
        
        # ID (para atualizar/deletar)
        tk.Label(campos_container, text="ID (para atualizar/deletar):", 
                bg='#f0f0f0', font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_id = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_id.grid(row=row, column=1, pady=5)
        row += 1
        
        # Nome
        tk.Label(campos_container, text="Nome *:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_nome = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_nome.grid(row=row, column=1, pady=5)
        row += 1
        
        # Email
        tk.Label(campos_container, text="Email *:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_email = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_email.grid(row=row, column=1, pady=5)
        row += 1
        
        # CPF/CNPJ - label dinâmico
        self.label_cpf_cnpj = tk.Label(campos_container, text="CPF/CNPJ *:", bg='#f0f0f0', font=('Arial', 10))
        self.label_cpf_cnpj.grid(row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_cpf = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_cpf.grid(row=row, column=1, pady=5)
        row += 1
        
        # Telefone
        tk.Label(campos_container, text="Telefone *:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_telefone = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_telefone.grid(row=row, column=1, pady=5)
        row += 1
        
        # Data Nascimento/Fundação
        tk.Label(campos_container, text="Data Nasc/Fund (YYYY-MM-DD):", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_dt_nasc = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_dt_nasc.grid(row=row, column=1, pady=5)
        row += 1
        
        # Login
        tk.Label(campos_container, text="Login:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_login = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_login.grid(row=row, column=1, pady=5)
        row += 1
        
        # Senha
        tk.Label(campos_container, text="Senha:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_senha = tk.Entry(campos_container, width=40, show='*', font=('Arial', 10))
        self.entry_senha.grid(row=row, column=1, pady=5)
        row += 1
        
        # Descrição (Estúdios)
        tk.Label(campos_container, text="Descrição (Estúdios):", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_descricao = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_descricao.grid(row=row, column=1, pady=5)
        row += 1
        
        # SEPARADOR PARA CAMPOS DE ENDEREÇO
        separador = tk.Frame(campos_container, height=2, bg='#ddd')
        separador.grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        tk.Label(campos_container, text="DADOS DE ENDEREÇO (Opcional - para criar novo endereço)", 
                bg='#f0f0f0', font=('Arial', 10, 'bold'), fg='#666').grid(
            row=row, column=0, columnspan=2, sticky='w', pady=5)
        row += 1
        
        # Campos de endereço individuais (editáveis)
        campos_endereco_simples = [
            ("CEP:", "entry_cep"),
            ("Rua:", "entry_rua"),
            ("Número:", "entry_numero"),
            ("Bairro:", "entry_bairro"),
            ("Complemento:", "entry_complemento")
        ]
        
        for label_text, attr_name in campos_endereco_simples:
            tk.Label(campos_container, text=label_text, bg='#f0f0f0', font=('Arial', 10)).grid(
                row=row, column=0, sticky='w', pady=5, padx=(0, 15))
            entry = tk.Entry(campos_container, width=40, font=('Arial', 10))
            entry.grid(row=row, column=1, pady=5)
            setattr(self, attr_name, entry)
            row += 1
        
        # UF - Combobox
        tk.Label(campos_container, text="UF:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        lista_uf = [uf['sigla'] for uf in self.estados_ibge]
        self.combo_uf = ttk.Combobox(campos_container, values=lista_uf, width=37, state='readonly', font=('Arial', 10))
        self.combo_uf.grid(row=row, column=1, pady=5)
        self.combo_uf.bind("<<ComboboxSelected>>", self.on_uf_selecionado)
        row += 1
        
        # Cidade - Combobox
        tk.Label(campos_container, text="Cidade:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.combo_cidade = ttk.Combobox(campos_container, values=[], width=37, state='readonly', font=('Arial', 10))
        self.combo_cidade.grid(row=row, column=1, pady=5)
        row += 1
        
        # Perfil
        tk.Label(campos_container, text="Perfil:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.combo_perfil = ttk.Combobox(campos_container, width=37, state='readonly', font=('Arial', 10))
        self.combo_perfil['values'] = ["1 - Administrador", "2 - Cliente", "3 - Estudio"]
        self.combo_perfil.grid(row=row, column=1, pady=5)
        
        # Pré-selecionar Admin para facilitar criação de usuários admin
        self.combo_perfil.set("1 - Administrador")
        
        # BOTÕES
        frame_botoes = tk.Frame(content_frame, bg='#f0f0f0')
        frame_botoes.pack(pady=30)
        
        # Título dos botões
        tk.Label(frame_botoes, text="AÇÕES ADMINISTRATIVAS", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#333').pack(pady=(0, 15))
        
        # Primeira linha de botões
        frame_botoes1 = tk.Frame(frame_botoes, bg='#f0f0f0')
        frame_botoes1.pack(pady=8)
        
        botoes1 = [
            ("CRIAR USUÁRIO", self.criar_usuario, '#27ae60', 15),
            ("LISTAR TODOS", self.listar_todos, '#3498db', 15),
            ("LISTAR ADMINS", self.listar_admins, '#8e44ad', 15),
            ("LISTAR CLIENTES", self.listar_clientes, '#e67e22', 15),
            ("LISTAR ESTÚDIOS", self.listar_estudios, '#2c3e50', 15)
        ]
        
        for texto, comando, cor, largura in botoes1:
            btn = tk.Button(frame_botoes1, text=texto, command=comando,
                           bg=cor, fg='white', font=('Arial', 10, 'bold'),
                           width=largura, height=2, cursor='hand2',
                           relief='raised', bd=2)
            btn.pack(side='left', padx=5)
        
        # Segunda linha de botões
        frame_botoes2 = tk.Frame(frame_botoes, bg='#f0f0f0')
        frame_botoes2.pack(pady=8)
        
        botoes2 = [
            ("BUSCAR POR ID", self.buscar_por_id, '#f39c12', 15),
            ("ATUALIZAR", self.atualizar_usuario, '#e74c3c', 15),
            ("DELETAR", self.deletar_usuario, '#c0392b', 15),
            ("LIMPAR CAMPOS", self.limpar_campos, '#95a5a6', 15),
            ("ADMIN PADRÃO", self.criar_admin_padrao, '#9b59b6', 15)
        ]
        
        for texto, comando, cor, largura in botoes2:
            btn = tk.Button(frame_botoes2, text=texto, command=comando,
                           bg=cor, fg='white', font=('Arial', 10, 'bold'),
                           width=largura, height=2, cursor='hand2',
                           relief='raised', bd=2)
            btn.pack(side='left', padx=5)
        
        # Área de resultados
        frame_resultados = tk.Frame(content_frame, bg='#f0f0f0', relief='groove', bd=2)
        frame_resultados.pack(pady=20, padx=40, fill='both', expand=True)
        
        tk.Label(frame_resultados, text="RESULTADOS DA CONSULTA:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#333').pack(anchor='w', padx=10, pady=(10, 5))
        
        # Scrollbar para o texto de resultados
        frame_text = tk.Frame(frame_resultados, bg='#f0f0f0')
        frame_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.text_resultados = tk.Text(frame_text, height=15, wrap=tk.WORD, font=('Consolas', 10),
                                      bg='#fafafa', fg='#333', relief='sunken', bd=2)
        scrollbar_text = tk.Scrollbar(frame_text, orient="vertical", command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar_text.set)
        
        self.text_resultados.pack(side="left", fill="both", expand=True)
        scrollbar_text.pack(side="right", fill="y")

        # Bind do scroll do mouse para o canvas principal
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para Windows
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        
        # Centralizar horizontalmente o conteúdo
        def centralizar_conteudo(event=None):
            canvas_width = canvas.winfo_width()
            frame_width = content_frame.winfo_reqwidth()
            x_pos = max(0, (canvas_width - frame_width) // 2)
            canvas.coords(canvas.find_all()[0], x_pos, 0)
        
        canvas.bind('<Configure>', centralizar_conteudo)
        scrollable_frame.bind('<Configure>', centralizar_conteudo)

    def criar_botao_voltar(self, parent):
        """Cria o botão voltar"""
        frame_voltar = tk.Frame(parent, bg='#f0f0f0')
        frame_voltar.pack(anchor='nw', pady=(0, 20))
        
        btn_voltar = tk.Button(frame_voltar, text="← VOLTAR", 
                              command=self.voltar_tela_principal,
                              bg='#34495e', fg='white', 
                              font=('Arial', 10, 'bold'),
                              width=12, height=2, cursor='hand2',
                              relief='raised', bd=2)
        btn_voltar.pack()

    def processar_endereco(self, id_endereco_atual=None):
        """Processa endereço: cria novo se dados fornecidos, senão mantém atual"""
        from datetime import datetime
        
        # Verificar se algum campo de endereço foi preenchido
        campos_endereco = {
            'cep': self.entry_cep.get().strip(),
            'rua': self.entry_rua.get().strip(),
            'numero': self.entry_numero.get().strip(),
            'bairro': self.entry_bairro.get().strip(),
            'cidade': self.combo_cidade.get().strip(),
            'uf': self.combo_uf.get().strip(),
            'complemento': self.entry_complemento.get().strip()
        }
        
        # Se nenhum campo de endereço foi preenchido, usar o primeiro endereço disponível
        if not any(campos_endereco.values()):
            if id_endereco_atual:
                return id_endereco_atual
            elif self.enderecos:
                return self.enderecos[0][0]  # Primeiro endereço da lista
            else:
                return 1  # ID padrão
        
        # Se algum campo foi preenchido, validar campos obrigatórios
        campos_obrigatorios = ['cep', 'rua', 'numero', 'bairro', 'cidade', 'uf']
        for campo in campos_obrigatorios:
            if not campos_endereco[campo]:
                raise ValueError(f"Campo {campo.upper()} é obrigatório para criar/atualizar endereço")
        
        cursor = self.dao.cursor
        agora = datetime.now()
        
        # Criar novo endereço usando a estrutura do EnderecoDAO
        cursor.execute("""
            INSERT INTO endereco (rua, numero, bairro, cidade, complemento, uf, cep, data_cadastro, data_atualizacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            campos_endereco['rua'],
            campos_endereco['numero'],
            campos_endereco['bairro'],
            campos_endereco['cidade'],
            campos_endereco['complemento'],
            campos_endereco['uf'],
            campos_endereco['cep'],
            agora,
            agora
        ))
        
        # Retornar ID do novo endereço
        
        return cursor.lastrowid

    def voltar_tela_principal(self):
        """Volta para a tela principal"""
        self.root.destroy()
        if self.callback_voltar:
            self.callback_voltar()

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
            self.combo_perfil.set("1 - Administrador")
            
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

    def criar_usuario(self):
        """Cria um novo usuário baseado no perfil selecionado"""
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
            
            # Obter perfil selecionado
            perfil_sel = self.combo_perfil.get()
            if not perfil_sel:
                messagebox.showwarning("Atenção", "Selecione um perfil")
                return
                
            id_perfil = int(perfil_sel.split(' - ')[0])
            
            # Obter dados opcionais
            dt_nasc = self.entry_dt_nasc.get().strip() or None
            descricao = self.entry_descricao.get().strip() or None
            
            # Processar endereço - usar primeiro endereço disponível se não especificado
            id_endereco = self.processar_endereco()
            
            cursor = self.dao.cursor
            
            # Criar baseado no perfil
            if id_perfil == 1:  # Administrador
                cursor.execute("""
                    INSERT INTO administrador (id_perfil, nome, email, login, senha)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_perfil, nome, email, login, senha))
                tipo_user = "ADMINISTRADOR"
                
            elif id_perfil == 2:  # Cliente
                cursor.execute("""
                    INSERT INTO cliente (id_perfil, id_endereco, nome, dt_nasc, genero, telefone, cpf, email, login, senha)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_perfil, id_endereco, nome, dt_nasc, 'Masculino', telefone, cpf, email, login, senha))
                tipo_user = "CLIENTE"
                
            elif id_perfil == 3:  # Estúdio
                cursor.execute("""
                    INSERT INTO estudio (id_perfil, id_endereco, nome, cnpj, descricao, login, senha)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (id_perfil, id_endereco, nome, cpf, descricao or 'Estúdio de tatuagem', login, senha))
                tipo_user = "ESTÚDIO"
            
            self.dao.conexao.commit()
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', f"✅ {tipo_user} CRIADO COM SUCESSO!\n\nNome: {nome}\nEmail: {email}\nLogin: {login}")
            self.limpar_campos()
            
        except Exception as e:
            self.dao.conexao.rollback()
            messagebox.showerror("Erro", f"Erro ao criar usuário: {str(e)}")


    def listar_todos(self):
        """Lista todos os usuários de todas as tabelas"""
        try:
            cursor = self.dao.cursor
            resultado = "📋 LISTA COMPLETA DE USUÁRIOS\n"
            resultado += "=" * 80 + "\n\n"
            
            # Administradores
            cursor.execute("""
                SELECT a.id_administrador, a.nome, a.email, a.login, 'Administrador' as tipo
                FROM administrador a
                ORDER BY a.id_administrador
            """)
            admins = cursor.fetchall()
            
            if admins:
                resultado += f"👑 ADMINISTRADORES ({len(admins)})\n"
                resultado += "-" * 40 + "\n"
                for admin in admins:
                    resultado += f"ID: {admin[0]} | Nome: {admin[1]} | Email: {admin[2]} | Login: {admin[3]}\n"
                resultado += "\n"
            
            # Clientes
            cursor.execute("""
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, c.login, 'Cliente' as tipo
                FROM cliente c
                WHERE c.id_perfil = 2
                ORDER BY c.id_cliente
            """)
            clientes = cursor.fetchall()
            
            if clientes:
                resultado += f"👤 CLIENTES ({len(clientes)})\n"
                resultado += "-" * 40 + "\n"
                for cliente in clientes:
                    resultado += f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | Telefone: {cliente[3]} | CPF: {cliente[4]} | Login: {cliente[5]}\n"
                resultado += "\n"
            
            # Estúdios
            cursor.execute("""
                SELECT e.id_estudio, e.nome, e.cnpj, e.descricao, e.login, 'Estudio' as tipo
                FROM estudio e
                WHERE e.id_perfil = 3
                ORDER BY e.id_estudio
            """)
            estudios = cursor.fetchall()
            
            if estudios:
                resultado += f"🏢 ESTÚDIOS ({len(estudios)})\n"
                resultado += "-" * 40 + "\n"
                for estudio in estudios:
                    resultado += f"ID: {estudio[0]} | Nome: {estudio[1]} | CNPJ: {estudio[2]} | Descrição: {estudio[3]} | Login: {estudio[4]}\n"
                resultado += "\n"
            
            total = len(admins) + len(clientes) + len(estudios)
            resultado += f"✅ Total geral: {total} usuários"
            
            if total == 0:
                resultado = "❌ Nenhum usuário encontrado no sistema."
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar usuários: {str(e)}")

    def listar_admins(self):
        """Lista apenas administradores"""
        try:
            cursor = self.dao.cursor
            cursor.execute("""
                SELECT a.id_administrador, a.nome, a.email, a.login
                FROM administrador a
                ORDER BY a.id_administrador
            """)
            
            admins = cursor.fetchall()
            
            if not admins:
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', "❌ Nenhum administrador encontrado.")
                return
            
            resultado = f"👑 ADMINISTRADORES ({len(admins)})\n"
            resultado += "=" * 60 + "\n\n"
            
            for i, admin in enumerate(admins, 1):
                resultado += f"#{i} - ID: {admin[0]}\n"
                resultado += f"   Nome: {admin[1]}\n"
                resultado += f"   Email: {admin[2]}\n"
                resultado += f"   Login: {admin[3]}\n"
                resultado += "-" * 60 + "\n"
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar administradores: {str(e)}")

    def listar_clientes(self):
        """Lista apenas clientes (perfil 2)"""
        try:
            cursor = self.dao.cursor
            cursor.execute("""
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, c.dt_nasc, c.login
                FROM cliente c
                WHERE c.id_perfil = 2
                ORDER BY c.id_cliente
            """)
            
            clientes = cursor.fetchall()
            
            if not clientes:
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', "❌ Nenhum cliente encontrado.")
                return
            
            resultado = f"👤 CLIENTES ({len(clientes)})\n"
            resultado += "=" * 60 + "\n\n"
            
            for i, cliente in enumerate(clientes, 1):
                resultado += f"#{i} - ID: {cliente[0]}\n"
                resultado += f"   Nome: {cliente[1]}\n"
                resultado += f"   Email: {cliente[2]}\n"
                resultado += f"   Telefone: {cliente[3]}\n"
                resultado += f"   CPF: {cliente[4]}\n"
                resultado += f"   Data Nasc: {cliente[5] if cliente[5] else 'Não informado'}\n"
                resultado += f"   Login: {cliente[6]}\n"
                resultado += "-" * 60 + "\n"
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar clientes: {str(e)}")

    def listar_estudios(self):
        """Lista apenas estúdios (perfil 3)"""
        try:
            cursor = self.dao.cursor
            cursor.execute("""
                SELECT e.id_estudio, e.nome, e.cnpj, e.descricao, e.login, e.tipo
                FROM estudio e
                WHERE e.id_perfil = 3
                ORDER BY e.id_estudio
            """)
            
            estudios = cursor.fetchall()
            
            if not estudios:
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', "❌ Nenhum estúdio encontrado.")
                return
            
            resultado = f"🏢 ESTÚDIOS ({len(estudios)})\n"
            resultado += "=" * 60 + "\n\n"
            
            for i, estudio in enumerate(estudios, 1):
                resultado += f"#{i} - ID: {estudio[0]}\n"
                resultado += f"   Nome: {estudio[1]}\n"
                resultado += f"   CNPJ: {estudio[2]}\n"
                resultado += f"   Descrição: {estudio[3]}\n"
                resultado += f"   Login: {estudio[4]}\n"
                resultado += f"   Tipo: {estudio[5] if estudio[5] else 'Não informado'}\n"
                resultado += "-" * 60 + "\n"
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar estúdios: {str(e)}")

    def buscar_por_id(self):
        """Busca usuário por ID em todas as tabelas"""
        try:
            id_usuario = self.entry_id.get().strip()
            if not id_usuario:
                messagebox.showwarning("Atenção", "Informe o ID do usuário")
                return
            
            cursor = self.dao.cursor
            resultado = f"🔍 BUSCA POR ID: {id_usuario}\n"
            resultado += "=" * 50 + "\n\n"
            
            encontrado = False
            
            # Buscar em administradores
            cursor.execute("""
                SELECT a.id_administrador, a.nome, a.email, a.login, 'Administrador' as tipo
                FROM administrador a
                WHERE a.id_administrador = %s
            """, (int(id_usuario),))
            
            admin = cursor.fetchone()
            if admin:
                resultado += f"👑 ADMINISTRADOR ENCONTRADO:\n"
                resultado += f"   ID: {admin[0]}\n"
                resultado += f"   Nome: {admin[1]}\n"
                resultado += f"   Email: {admin[2]}\n"
                resultado += f"   Login: {admin[3]}\n"
                resultado += f"   Tipo: {admin[4]}\n\n"
                encontrado = True
                
                # Preencher campos para edição
                self.limpar_campos()
                self.entry_id.insert(0, str(admin[0]))
                self.entry_nome.insert(0, admin[1])
                self.entry_email.insert(0, admin[2])
                self.entry_login.insert(0, admin[3])
                self.combo_perfil.set("1 - Administrador")
            
            # Buscar em clientes
            cursor.execute("""
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, c.dt_nasc, c.login, c.genero, c.id_endereco
                FROM cliente c
                WHERE c.id_cliente = %s AND c.id_perfil = 2
            """, (int(id_usuario),))
            
            cliente = cursor.fetchone()
            if cliente:
                resultado += f"👤 CLIENTE ENCONTRADO:\n"
                resultado += f"   ID: {cliente[0]}\n"
                resultado += f"   Nome: {cliente[1]}\n"
                resultado += f"   Email: {cliente[2]}\n"
                resultado += f"   Telefone: {cliente[3]}\n"
                resultado += f"   CPF: {cliente[4]}\n"
                resultado += f"   Data Nasc: {cliente[5] if cliente[5] else 'Não informado'}\n"
                resultado += f"   Login: {cliente[6]}\n"
                resultado += f"   Gênero: {cliente[7] if cliente[7] else 'Não informado'}\n\n"
                encontrado = True
                
                # Preencher campos para edição
                self.limpar_campos()
                self.entry_id.insert(0, str(cliente[0]))
                self.entry_nome.insert(0, cliente[1])
                self.entry_email.insert(0, cliente[2])
                self.entry_telefone.insert(0, cliente[3])
                self.entry_cpf.insert(0, cliente[4])
                if cliente[5]:
                    self.entry_dt_nasc.insert(0, str(cliente[5]))
                self.entry_login.insert(0, cliente[6])
                self.combo_perfil.set("2 - Cliente")
            
            # Buscar em estúdios
            cursor.execute("""
                SELECT e.id_estudio, e.nome, e.cnpj, e.descricao, e.login, e.tipo, e.id_endereco
                FROM estudio e
                WHERE e.id_estudio = %s AND e.id_perfil = 3
            """, (int(id_usuario),))
            
            estudio = cursor.fetchone()
            if estudio:
                resultado += f"🏢 ESTÚDIO ENCONTRADO:\n"
                resultado += f"   ID: {estudio[0]}\n"
                resultado += f"   Nome: {estudio[1]}\n"
                resultado += f"   CNPJ: {estudio[2]}\n"
                resultado += f"   Descrição: {estudio[3]}\n"
                resultado += f"   Login: {estudio[4]}\n"
                resultado += f"   Tipo: {estudio[5] if estudio[5] else 'Não informado'}\n\n"
                encontrado = True
                
                # Preencher campos para edição
                self.limpar_campos()
                self.entry_id.insert(0, str(estudio[0]))
                self.entry_nome.insert(0, estudio[1])
                self.entry_cpf.insert(0, estudio[2])  # CNPJ no campo CPF
                self.entry_descricao.insert(0, estudio[3])
                self.entry_login.insert(0, estudio[4])
                self.combo_perfil.set("3 - Estudio")
            
            if not encontrado:
                resultado += f"❌ Nenhum usuário encontrado com ID: {id_usuario}"
            else:
                resultado += "✅ Dados carregados nos campos para edição!"
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número válido")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {str(e)}")

    def atualizar_usuario(self):
        """Atualiza usuário baseado no perfil selecionado - COM ENDEREÇO DAO"""
        try:
            id_usuario = self.entry_id.get().strip()
            if not id_usuario:
                messagebox.showwarning("Atenção", "Informe o ID do usuário para atualizar")
                return
            
            # Validar campos obrigatórios
            nome = self.entry_nome.get().strip()
            email = self.entry_email.get().strip()
            
            if not all([nome, email]):
                messagebox.showwarning("Atenção", "Nome e Email são obrigatórios")
                return
            
            # Obter perfil selecionado
            perfil_sel = self.combo_perfil.get()
            if not perfil_sel:
                messagebox.showwarning("Atenção", "Selecione um perfil")
                return
                
            id_perfil = int(perfil_sel.split(' - ')[0])
            
            cursor = self.dao.cursor
            
            # Atualizar baseado no perfil
            if id_perfil == 1:  # Administrador
                login = self.entry_login.get().strip()
                senha = self.entry_senha.get().strip()
                
                if senha:  # Se senha foi fornecida, atualizar também
                    cursor.execute("""
                        UPDATE administrador 
                        SET nome = %s, email = %s, login = %s, senha = %s
                        WHERE id_administrador = %s
                    """, (nome, email, login, senha, int(id_usuario)))
                else:  # Manter senha atual
                    cursor.execute("""
                        UPDATE administrador 
                        SET nome = %s, email = %s, login = %s
                        WHERE id_administrador = %s
                    """, (nome, email, login, int(id_usuario)))
                
                tipo_user = "ADMINISTRADOR"
                
            elif id_perfil == 2:  # Cliente
                # Buscar dados atuais do cliente
                cursor.execute("""
                    SELECT nome, email, telefone, cpf, dt_nasc, login, senha, id_endereco
                    FROM cliente WHERE id_cliente = %s AND id_perfil = 2
                """, (int(id_usuario),))
                
                dados_atuais = cursor.fetchone()
                if not dados_atuais:
                    messagebox.showwarning("Atenção", f"Cliente com ID {id_usuario} não encontrado")
                    return
                
                # Usar dados do formulário se preenchidos, senão manter os atuais
                nome = self.entry_nome.get().strip() or dados_atuais[0]
                email = self.entry_email.get().strip() or dados_atuais[1]
                telefone = self.entry_telefone.get().strip() or dados_atuais[2]
                cpf = self.entry_cpf.get().strip() or dados_atuais[3]
                dt_nasc = self.entry_dt_nasc.get().strip() or dados_atuais[4]
                login = self.entry_login.get().strip() or dados_atuais[5]
                senha = self.entry_senha.get().strip() or dados_atuais[6]
                
                # Processar endereço
                id_endereco = self.processar_endereco(dados_atuais[7])
                
                cursor.execute("""
                    UPDATE cliente 
                    SET nome = %s, email = %s, telefone = %s, cpf = %s, dt_nasc = %s, 
                        login = %s, senha = %s, id_endereco = %s
                    WHERE id_cliente = %s AND id_perfil = 2
                """, (nome, email, telefone, cpf, dt_nasc, login, senha, id_endereco, int(id_usuario)))
                
                tipo_user = "CLIENTE"
                
            elif id_perfil == 3:  # Estúdio
                # Buscar dados atuais do estúdio
                cursor.execute("""
                    SELECT nome, cnpj, descricao, login, senha, id_endereco
                    FROM estudio WHERE id_estudio = %s AND id_perfil = 3
                """, (int(id_usuario),))
                
                dados_atuais = cursor.fetchone()
                if not dados_atuais:
                    messagebox.showwarning("Atenção", f"Estúdio com ID {id_usuario} não encontrado")
                    return
                
                # Usar dados do formulário se preenchidos, senão manter os atuais
                nome = self.entry_nome.get().strip() or dados_atuais[0]
                cnpj = self.entry_cpf.get().strip() or dados_atuais[1]  # CNPJ está no campo CPF
                descricao = self.entry_descricao.get().strip() or dados_atuais[2]
                login = self.entry_login.get().strip() or dados_atuais[3]
                senha = self.entry_senha.get().strip() or dados_atuais[4]
                
                # Processar endereço
                id_endereco = self.processar_endereco(dados_atuais[5])
                
                cursor.execute("""
                    UPDATE estudio 
                    SET nome = %s, cnpj = %s, descricao = %s, login = %s, senha = %s, id_endereco = %s
                    WHERE id_estudio = %s AND id_perfil = 3
                """, (nome, cnpj, descricao, login, senha, id_endereco, int(id_usuario)))
                
                tipo_user = "ESTÚDIO"
            
            # Verificar se algum registro foi atualizado
            if cursor.rowcount == 0:
                messagebox.showwarning("Atenção", f"Nenhum {tipo_user.lower()} encontrado com ID: {id_usuario}")
                return
            
            self.dao.conexao.commit()
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', 
                f"✅ {tipo_user} ATUALIZADO COM SUCESSO!\n\n"
                f"ID: {id_usuario}\n"
                f"Nome: {nome}\n"
                f"Email: {email}\n"
                f"{'Endereço: Atualizado' if any([self.entry_cep.get().strip(), self.entry_rua.get().strip()]) else 'Endereço: Mantido'}\n"
                f"{'Senha: Atualizada' if self.entry_senha.get().strip() else 'Senha: Mantida'}"
            )
            
            # Limpar campos após sucesso
            self.limpar_campos()
            
        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            self.dao.conexao.rollback()
            messagebox.showerror("Erro", f"Erro ao atualizar usuário: {str(e)}")


    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        campos = [
            'entry_id', 'entry_nome', 'entry_email', 'entry_cpf', 'entry_telefone',
            'entry_dt_nasc', 'entry_login', 'entry_senha', 'entry_descricao',
            'entry_cep', 'entry_rua', 'entry_numero', 'entry_bairro',
            'entry_complemento'
        ]
        
        for campo in campos:
            if hasattr(self, campo):
                getattr(self, campo).delete(0, tk.END)
        
        # Limpar combos
        if hasattr(self, 'combo_perfil'):
            self.combo_perfil.set('')
        if hasattr(self, 'combo_uf'):
            self.combo_uf.set('')
        if hasattr(self, 'combo_cidade'):
            self.combo_cidade.set('')
        
        # Limpar área de resultados
        if hasattr(self, 'text_resultados'):
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', "Campos limpos! Pronto para nova operação.")

    def deletar_usuario(self):
        """Deleta usuário baseado no perfil selecionado"""
        try:
            id_usuario = self.entry_id.get().strip()
            if not id_usuario:
                messagebox.showwarning("Atenção", "Informe o ID do usuário para deletar")
                return
            
            # Obter perfil selecionado
            perfil_sel = self.combo_perfil.get()
            if not perfil_sel:
                messagebox.showwarning("Atenção", "Selecione um perfil")
                return
                
            id_perfil = int(perfil_sel.split(' - ')[0])
            
            # Confirmar exclusão
            nome_tabela = {1: "Administrador", 2: "Cliente", 3: "Estúdio"}[id_perfil]
            resposta = messagebox.askyesno(
                "Confirmar Exclusão", 
                f"Tem certeza que deseja deletar o {nome_tabela} com ID {id_usuario}?\n\nEsta ação não pode ser desfeita!"
            )
            
            if not resposta:
                return
            
            cursor = self.dao.cursor
            
            # Deletar baseado no perfil
            if id_perfil == 1:  # Administrador
                cursor.execute("DELETE FROM administrador WHERE id_administrador = %s", (int(id_usuario),))
                tipo_user = "ADMINISTRADOR"
                
            elif id_perfil == 2:  # Cliente
                cursor.execute("DELETE FROM cliente WHERE id_cliente = %s AND id_perfil = 2", (int(id_usuario),))
                tipo_user = "CLIENTE"
                
            elif id_perfil == 3:  # Estúdio
                cursor.execute("DELETE FROM estudio WHERE id_estudio = %s AND id_perfil = 3", (int(id_usuario),))
                tipo_user = "ESTÚDIO"
            
            # Verificar se algum registro foi deletado
            if cursor.rowcount == 0:
                messagebox.showwarning("Atenção", f"Nenhum {tipo_user.lower()} encontrado com ID: {id_usuario}")
                return
            
            self.dao.conexao.commit()
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', 
                f"🗑️ {tipo_user} DELETADO COM SUCESSO!\n\n"
                f"ID: {id_usuario} foi removido permanentemente do sistema."
            )
            
            # Limpar campos após deletar
            self.limpar_campos()
            
        except ValueError:
            messagebox.showerror("Erro", "ID deve ser um número válido")
        except Exception as e:
            self.dao.conexao.rollback()
            messagebox.showerror("Erro", f"Erro ao deletar usuário: {str(e)}")

