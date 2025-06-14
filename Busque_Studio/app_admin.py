#app_admin.py
import tkinter as tk
from tkinter import messagebox, ttk
from clienteDAO import ClienteDAO
from cliente import Cliente
from administrador import Administrador


class AppAdmin:
    def __init__(self, root, callback_voltar=None):
        self.dao = ClienteDAO()
        self.root = root
        self.callback_voltar = callback_voltar
        self.perfil_id = 3  # PERFIL FIXO: Admin
        self.perfil_nome = "Admin"
        self.modo_admin = True  # MODO ADMIN ATIVADO
        
        self.root.title("Área Administrativa - BusqueStudios")
        self.root.state('zoomed')  # Abre em tela cheia no Windows
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
        
        # ID Cliente (para atualizar/deletar)
        tk.Label(campos_container, text="ID Cliente (para atualizar/deletar):", 
                bg='#f0f0f0', font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.entry_id_cliente = tk.Entry(campos_container, width=40, font=('Arial', 10))
        self.entry_id_cliente.grid(row=row, column=1, pady=5)
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
            tk.Label(campos_container, text=label_text, bg='#f0f0f0', font=('Arial', 10)).grid(
                row=row, column=0, sticky='w', pady=5, padx=(0, 15))
            
            # Para o campo senha, usar show='*' para ocultar texto
            if attr_name == "entry_senha":
                entry = tk.Entry(campos_container, width=40, show='*', font=('Arial', 10))
            else:
                entry = tk.Entry(campos_container, width=40, font=('Arial', 10))
                
            entry.grid(row=row, column=1, pady=5)
            setattr(self, attr_name, entry)
            row += 1

        # Endereço
        tk.Label(campos_container, text="Endereço:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.combo_endereco = ttk.Combobox(campos_container, width=37, state='readonly', font=('Arial', 10))
        self.combo_endereco['values'] = [f"{id_end} - {endereco}" for id_end, endereco in self.enderecos]
        self.combo_endereco.grid(row=row, column=1, pady=5)
        row += 1
        
        # Perfil
        tk.Label(campos_container, text="Perfil:", bg='#f0f0f0', font=('Arial', 10)).grid(
            row=row, column=0, sticky='w', pady=5, padx=(0, 15))
        self.combo_perfil = ttk.Combobox(campos_container, width=37, state='readonly', font=('Arial', 10))
        self.combo_perfil['values'] = ["1 - Cliente", "2 - Estúdio", "3 - Admin"]
        self.combo_perfil.grid(row=row, column=1, pady=5)
        
        # Pré-selecionar Admin para facilitar criação de usuários admin
        self.combo_perfil.set("3 - Admin")
        
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
            ("CRIAR USUÁRIO", self.criar_cliente, '#27ae60', 18),
            ("LISTAR TODOS", self.listar_clientes, '#3498db', 18),
            ("BUSCAR POR ID", self.buscar_por_id, '#f39c12', 18),
            ("ATUALIZAR", self.atualizar_cliente, '#e67e22', 18)
        ]
        
        for texto, comando, cor, largura in botoes1:
            btn = tk.Button(frame_botoes1, text=texto, command=comando,
                           bg=cor, fg='white', font=('Arial', 10, 'bold'),
                           width=largura, height=2, cursor='hand2',
                           relief='raised', bd=2)
            btn.pack(side='left', padx=8)
        
        # Segunda linha de botões
        frame_botoes2 = tk.Frame(frame_botoes, bg='#f0f0f0')
        frame_botoes2.pack(pady=8)
        
        botoes2 = [
            ("DELETAR", self.deletar_cliente, '#e74c3c', 18),
            ("LIMPAR CAMPOS", self.limpar_campos, '#95a5a6', 18),
            ("CRIAR ADMIN PADRÃO", self.criar_admin_padrao, '#8e44ad', 20)
        ]
        
        for texto, comando, cor, largura in botoes2:
            btn = tk.Button(frame_botoes2, text=texto, command=comando,
                           bg=cor, fg='white', font=('Arial', 10, 'bold'),
                           width=largura, height=2, cursor='hand2',
                           relief='raised', bd=2)
            btn.pack(side='left', padx=8)
        
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
        
        # Bind para Linux
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Centralizar horizontalmente o conteúdo
        def centralizar_conteudo(event=None):
            canvas_width = canvas.winfo_width()
            frame_width = content_frame.winfo_reqwidth()
            x_pos = max(0, (canvas_width - frame_width) // 2)
            canvas.coords(canvas.find_all()[0], x_pos, 0)
        
        canvas.bind('<Configure>', centralizar_conteudo)
        scrollable_frame.bind('<Configure>', centralizar_conteudo)

    def criar_botao_voltar(self, parent):
        """Cria botão Voltar no canto superior esquerdo"""
        frame_voltar = tk.Frame(parent, bg='#f0f0f0')
        frame_voltar.pack(fill='x', pady=(0, 10))
        
        btn_voltar = tk.Button(frame_voltar, 
                              text="← Voltar",
                              command=self.voltar_tela_principal,
                              bg='#95a5a6', fg='white',
                              font=('Arial', 11, 'bold'),
                              width=12, height=2,
                              cursor='hand2',
                              relief='raised', bd=2)
        btn_voltar.pack(side='left', pady=5)
    
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
                self.text_resultados.insert('1.0', f"✅ USUÁRIO CRIADO COM SUCESSO!\n\n{resultado}")
                self.limpar_campos()
            else:
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', f"❌ ERRO AO CRIAR USUÁRIO!\n\n{resultado}")
                
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
        
        # Limpar área de resultados
        self.text_resultados.delete('1.0', tk.END)
        self.text_resultados.insert('1.0', "Campos limpos! Pronto para nova operação.")

    def listar_clientes(self):
        """Lista todos os clientes formatado linha por linha"""
        try:
            # Buscar dados diretamente do banco para melhor formatação
            cursor = self.dao.cursor
            cursor.execute("""
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, 
                       c.dt_nasc, c.login, 
                       CASE c.id_perfil 
                           WHEN 1 THEN 'Cliente'
                           WHEN 2 THEN 'Estúdio' 
                           WHEN 3 THEN 'Admin'
                           ELSE 'Desconhecido'
                       END as perfil,
                       CONCAT(e.rua, ', ', e.numero, ' - ', e.bairro, ', ', e.cidade, '/', e.uf) as endereco_completo
                FROM cliente c
                LEFT JOIN endereco e ON c.id_endereco = e.id_endereco
                ORDER BY c.id_cliente
            """)
            
            usuarios = cursor.fetchall()
            
            if not usuarios:
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', "❌ Nenhum usuário encontrado no sistema.")
                return
            
            # Formatação melhorada
            resultado = f"📋 LISTA DE TODOS OS USUÁRIOS ({len(usuarios)} encontrados)\n"
            resultado += "=" * 80 + "\n\n"
            
            for i, user in enumerate(usuarios, 1):
                id_cliente, nome, email, telefone, cpf, dt_nasc, login, perfil, endereco = user
                
                resultado += f"👤 USUÁRIO #{i} (ID: {id_cliente})\n"
                resultado += f"   Nome: {nome}\n"
                resultado += f"   Email: {email}\n"
                resultado += f"   Telefone: {telefone}\n"
                resultado += f"   CPF: {cpf}\n"
                resultado += f"   Data Nascimento: {dt_nasc if dt_nasc else 'Não informado'}\n"
                resultado += f"   Login: {login if login else 'Não definido'}\n"
                resultado += f"   Perfil: {perfil}\n"
                resultado += f"   Endereço: {endereco if endereco else 'Não informado'}\n"
                resultado += "-" * 80 + "\n"
            
            resultado += f"\n✅ Total de usuários listados: {len(usuarios)}"
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar usuários: {str(e)}")

    def buscar_por_id(self):
        """Busca cliente por ID com formatação melhorada"""
        try:
            id_cliente = self.entry_id_cliente.get().strip()
            if not id_cliente:
                messagebox.showwarning("Atenção", "Informe o ID do cliente")
                return
            
            # Buscar dados formatados
            cursor = self.dao.cursor
            cursor.execute("""
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, 
                       c.dt_nasc, c.login,
                       CASE c.id_perfil 
                           WHEN 1 THEN 'Cliente'
                           WHEN 2 THEN 'Estúdio' 
                           WHEN 3 THEN 'Admin'
                           ELSE 'Desconhecido'
                       END as perfil,
                       CONCAT(e.rua, ', ', e.numero, ' - ', e.bairro, ', ', e.cidade, '/', e.uf) as endereco_completo
                FROM cliente c
                LEFT JOIN endereco e ON c.id_endereco = e.id_endereco
                WHERE c.id_cliente = %s
            """, (int(id_cliente),))
            
            user = cursor.fetchone()
            
            if not user:
                self.text_resultados.delete('1.0', tk.END)
                self.text_resultados.insert('1.0', f"❌ Usuário com ID {id_cliente} não encontrado.")
                return
            
            id_cliente, nome, email, telefone, cpf, dt_nasc, login, perfil, endereco = user
            
            resultado = f"🔍 USUÁRIO ENCONTRADO (ID: {id_cliente})\n"
            resultado += "=" * 50 + "\n\n"
            resultado += f"👤 Nome: {nome}\n"
            resultado += f"📧 Email: {email}\n"
            resultado += f"📱 Telefone: {telefone}\n"
            resultado += f"🆔 CPF: {cpf}\n"
            resultado += f"📅 Data Nascimento: {dt_nasc if dt_nasc else 'Não informado'}\n"
            resultado += f"🔑 Login: {login if login else 'Não definido'}\n"
            resultado += f"👥 Perfil: {perfil}\n"
            resultado += f"🏠 Endereço: {endereco if endereco else 'Não informado'}\n"
            resultado += "\n✅ Consulta realizada com sucesso!"
            
            self.text_resultados.delete('1.0', tk.END)
            self.text_resultados.insert('1.0', resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuário: {str(e)}")

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
            if "sucesso" in resultado.lower():
                self.text_resultados.insert('1.0', f"✅ USUÁRIO ATUALIZADO COM SUCESSO!\n\nID: {id_cliente}\n{resultado}")
            else:
                self.text_resultados.insert('1.0', f"❌ ERRO AO ATUALIZAR USUÁRIO!\n\n{resultado}")
            
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
            resposta = messagebox.askyesno("Confirmar Exclusão", 
                                         f"⚠️ ATENÇÃO!\n\nTem certeza que deseja DELETAR permanentemente o usuário ID {id_cliente}?\n\nEsta ação não pode ser desfeita!")
            if resposta:
                resultado = self.dao.deletar(int(id_cliente))
                
                self.text_resultados.delete('1.0', tk.END)
                if "sucesso" in resultado.lower():
                    self.text_resultados.insert('1.0', f"✅ USUÁRIO DELETADO COM SUCESSO!\n\nID: {id_cliente}\n{resultado}")
                else:
                    self.text_resultados.insert('1.0', f"❌ ERRO AO DELETAR USUÁRIO!\n\n{resultado}")
                
                self.limpar_campos()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar: {str(e)}")