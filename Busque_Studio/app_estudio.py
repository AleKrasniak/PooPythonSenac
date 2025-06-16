import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from estudioDAO import EstudioDAO
from alvaraDAO import AlvaraDAO
from alvara import Alvara
from typing import Optional

class AppEstudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Estúdio - BusqueStudios")
        self.root.state('zoomed')  #tela cheia no Windows

        self.root.configure(bg='#f0f0f0')

        self.estudio_dao = EstudioDAO()
        self.alvara_dao = AlvaraDAO()
        self.perfil_id = 3
        self.id_estudio_cadastrado = None
        self.estados = self.carregar_ufs()
        self.criar_interface()

    def carregar_ufs(self):
        """Carrega a lista de UFs da API do IBGE"""
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
        """Carrega as cidades quando um estado é selecionado"""
        uf = self.combo_uf.get()
        estado = next((e for e in self.estados if e['sigla'] == uf), None)
        if not estado:
            self.combo_cidade['values'] = []
            return
        
        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado['id']}/municipios"
        try:
            resposta = requests.get(url, timeout=5)
            resposta.raise_for_status()
            cidades = [cidade['nome'] for cidade in resposta.json()]
            cidades.sort()
            self.combo_cidade['values'] = cidades
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar cidades: {e}")

    def criar_interface(self):
        """Cria a interface gráfica do aplicativo"""
        # Container principal
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True)

        # Canvas e scrollbar para todo o conteúdo
        canvas = tk.Canvas(main_container, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Container principal que ocupa toda a largura
        content_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        content_container.pack(fill='both', expand=True)

        # Título centralizado
        title_frame = tk.Frame(content_container, bg='#f0f0f0')
        title_frame.pack(pady=(20, 30), fill='x')
        tk.Label(title_frame, text="CADASTRO DE ESTÚDIO", font=('Arial', 16, 'bold'), 
                bg='#f0f0f0', fg='#333').pack()

        # Frame principal centralizado para os campos
        center_frame = tk.Frame(content_container, bg='#f0f0f0')
        center_frame.pack(expand=True)

        # Frame principal para os campos organizados em colunas
        frame_principal = tk.Frame(center_frame, bg='#f0f0f0')
        frame_principal.pack()

        # Configurar colunas com peso igual
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)

        # Frame para coluna esquerda
        frame_esquerda = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_esquerda.grid(row=0, column=0, padx=(0, 40), sticky='n')

        # Frame para coluna direita  
        frame_direita = tk.Frame(frame_principal, bg='#f0f0f0')
        frame_direita.grid(row=0, column=1, padx=(40, 0), sticky='n')

        # Campos da coluna esquerda
        campos_esquerda = [
            ("Nome do Estúdio *:", "entry_nome"),
            ("CNPJ * (14 dígitos):", "entry_cnpj"),
            ("Email *:", "entry_email"),
            ("Telefone *:", "entry_telefone"),
            ("Descrição:", "text_descricao"),
            ("CEP * (12345-678):", "entry_cep"),
            ("Rua:", "entry_rua"),
            ("Número:", "entry_numero")
        ]

        # Campos da coluna direita
        campos_direita = [
            ("Bairro:", "entry_bairro"),
            ("Complemento:", "entry_complemento"),
            ("Login *:", "entry_login"),
            ("Senha *:", "entry_senha", True),
            ("Confirme a Senha *:", "entry_confirmar_senha", True),
            ("URL da Foto:", "entry_foto_perfil"),
            ("UF *:", "combo_uf"),
            ("Cidade *:", "combo_cidade"),
            ("Tipo *:", "combo_tipo")
        ]

        # Criar campos da coluna esquerda
        self.criar_campos(frame_esquerda, campos_esquerda)
        
        # Criar campos da coluna direita
        self.criar_campos(frame_direita, campos_direita)

        # Frame para botões centralizados
        frame_botoes = tk.Frame(center_frame, bg='#f0f0f0')
        frame_botoes.pack(pady=40)

        # Botão Continuar (substituiu o CADASTRAR)
        tk.Button(frame_botoes, text="CONTINUAR", command=self.continuar_cadastro,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'), 
                 width=25, height=2).pack(pady=5)

        # Botão Limpar
        tk.Button(frame_botoes, text="LIMPAR", command=self.limpar_campos,
                 bg='#607D8B', fg='white', font=('Arial', 10, 'bold'),
                 width=15, height=2).pack(pady=5)

        # Bind scroll do mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind para canvas e scrollable_frame
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Centralizar o canvas horizontalmente
        def centralizar_canvas(event=None):
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            content_width = scrollable_frame.winfo_reqwidth()
            if content_width < canvas_width:
                x = (canvas_width - content_width) // 2
                canvas.create_window((x, 0), window=scrollable_frame, anchor="n")
            else:
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.bind('<Configure>', centralizar_canvas)
        self.root.after(100, centralizar_canvas)

    def criar_campos(self, parent_frame, campos):
        """Cria os campos de entrada em um frame específico"""
        row = 0
        for campo_info in campos:
            label_text = campo_info[0]
            attr_name = campo_info[1]
            is_password = len(campo_info) > 2 and campo_info[2]
            
            # Frame para cada linha
            linha_frame = tk.Frame(parent_frame, bg='#f0f0f0')
            linha_frame.grid(row=row, column=0, sticky='ew', pady=3)
            linha_frame.columnconfigure(1, weight=1)
            
            # Label com largura fixa
            tk.Label(linha_frame, text=label_text, bg='#f0f0f0', 
                    font=('Arial', 10), width=20, anchor='w').grid(
                    row=0, column=0, sticky='w', padx=(0, 10))
            
            # Widget de entrada
            if attr_name == "text_descricao":
                widget = tk.Text(linha_frame, width=30, height=4, font=('Arial', 10))
            elif attr_name == "combo_uf":
                widget = ttk.Combobox(linha_frame, values=[e['sigla'] for e in self.estados], 
                                    width=27, state='readonly')
                widget.bind("<<ComboboxSelected>>", self.on_uf_selecionado)
            elif attr_name == "combo_cidade":
                widget = ttk.Combobox(linha_frame, values=[], width=27, state='readonly')
            elif attr_name == "combo_tipo":
                widget = ttk.Combobox(linha_frame, 
                                    values=['Tatuagem', 'Fotografia', 'Música', 'Arte', 'Design', 'Áudio', 'Vídeo'], 
                                    width=27, state='readonly')
            else:
                widget = tk.Entry(linha_frame, width=30, show='*' if is_password else '', 
                                font=('Arial', 10))
            
            widget.grid(row=0, column=1, sticky='w')
            setattr(self, attr_name, widget)
            row += 1

    def validar_cep(self, cep: str) -> Optional[str]:
        """Valida e formata o CEP"""
        cep = cep.strip()
        if len(cep) == 8 and cep.isdigit():
            return f"{cep[:5]}-{cep[5:]}"
        elif len(cep) == 9 and cep[5] == '-' and cep.replace('-', '').isdigit():
            return cep
        return None

    def continuar_cadastro(self):
        """Valida dados do estúdio e vai para tela de alvará"""
        try:
            # Obter valores dos campos
            nome = self.entry_nome.get().strip()
            cnpj = self.entry_cnpj.get().strip()
            email = self.entry_email.get().strip()
            telefone = self.entry_telefone.get().strip()
            descricao = self.text_descricao.get("1.0", tk.END).strip()
            cep = self.validar_cep(self.entry_cep.get().strip())
            rua = self.entry_rua.get().strip()
            numero = self.entry_numero.get().strip()
            bairro = self.entry_bairro.get().strip()
            complemento = self.entry_complemento.get().strip()
            uf = self.combo_uf.get().strip()
            cidade = self.combo_cidade.get().strip()
            tipo = self.combo_tipo.get().strip()
            login = self.entry_login.get().strip()
            senha = self.entry_senha.get().strip()
            confirmar_senha = self.entry_confirmar_senha.get().strip()
            foto_perfil = self.entry_foto_perfil.get().strip()

            # Validações básicas
            if not all([nome, cnpj, email, telefone, cep, uf, cidade, tipo, login, senha]):
                raise ValueError("Preencha todos os campos obrigatórios (*)")

            if len(cnpj) != 14 or not cnpj.isdigit():
                raise ValueError("CNPJ deve ter 14 dígitos numéricos")

            if not cep:
                raise ValueError("CEP inválido. Formato: 12345-678 ou 12345678")

            if len(senha) < 6:
                raise ValueError("Senha deve ter pelo menos 6 caracteres")

            if senha != confirmar_senha:
                raise ValueError("As senhas não coincidem")

            # Verifica se login já existe
            if self.estudio_dao.buscar_por_login(login):
                raise ValueError("Login já está em uso")

            # Prepara os dados para o DAO
            self.dados_estudio = {
                'id_perfil': self.perfil_id,
                'nome': nome,
                'cnpj': cnpj,
                'descricao': descricao,
                'login': login,
                'senha': senha,
                'tipo': tipo,
                'email': email,
                'telefone': telefone,
                'foto_perfil': foto_perfil if foto_perfil else None,
                'rua': rua if rua else "Não informado",
                'numero': int(numero) if numero.isdigit() else 0,
                'bairro': bairro if bairro else "Não informado",
                'cidade': cidade,
                'complemento': complemento if complemento else "Não informado",
                'uf': uf,
                'cep': cep
            }

            # Vai para tela de alvará
            self.mostrar_tela_alvara()

        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na validação: {str(e)}")

    def mostrar_tela_alvara(self):
        """Exibe a tela de cadastro de alvará"""
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Container principal
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True)

        # Canvas e scrollbar
        canvas = tk.Canvas(main_container, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Container de conteúdo centralizado
        content_container = tk.Frame(scrollable_frame, bg='#f0f0f0')
        content_container.pack(fill='both', expand=True)

        # Frame principal centralizado
        center_frame = tk.Frame(content_container, bg='#f0f0f0')
        center_frame.pack(expand=True)

        # Título
        title_frame = tk.Frame(center_frame, bg='#f0f0f0')
        title_frame.pack(pady=(30, 40))
        tk.Label(title_frame, text="CADASTRO DE ALVARÁ", 
                font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333').pack()

        # Container principal para os alvarás
        alvaras_container = tk.Frame(center_frame, bg='#f0f0f0')
        alvaras_container.pack()

        # Frame para os dois alvarás lado a lado
        alvaras_frame = tk.Frame(alvaras_container, bg='#f0f0f0')
        alvaras_frame.pack(pady=20)

        # Alvará de Funcionamento
        funcionamento_frame = tk.LabelFrame(alvaras_frame, text="Alvará de Funcionamento *", 
                                          font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#333',
                                          padx=20, pady=15)
        funcionamento_frame.pack(side='left', padx=(0, 30), fill='both', expand=True)

        # Campos do Alvará de Funcionamento
        tk.Label(funcionamento_frame, text="Número do Alvará *:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(5, 2))
        self.entry_alvara_funcionamento = tk.Entry(funcionamento_frame, width=35, font=('Arial', 10))
        self.entry_alvara_funcionamento.pack(pady=(0, 15))

        tk.Label(funcionamento_frame, text="Data de Emissão *:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(0, 2))
        self.entry_data_emissao_func = tk.Entry(funcionamento_frame, width=35, font=('Arial', 10))
        self.entry_data_emissao_func.pack(pady=(0, 15))
        self.entry_data_emissao_func.insert(0, "DD/MM/AAAA")

        tk.Label(funcionamento_frame, text="Data de Validade *:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(0, 2))
        self.entry_data_validade_func = tk.Entry(funcionamento_frame, width=35, font=('Arial', 10))
        self.entry_data_validade_func.pack(pady=(0, 15))
        self.entry_data_validade_func.insert(0, "DD/MM/AAAA")

        tk.Label(funcionamento_frame, text="Status:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(0, 2))
        self.combo_status_func = ttk.Combobox(funcionamento_frame, values=['Ativo', 'Vencido', 'Pendente'], 
                                            width=32, state='readonly')
        self.combo_status_func.set('Ativo')
        self.combo_status_func.pack(pady=(0, 10))

        # Licença Sanitária
        sanitaria_frame = tk.LabelFrame(alvaras_frame, text="Licença Sanitária *", 
                                      font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#333',
                                      padx=20, pady=15)
        sanitaria_frame.pack(side='right', padx=(30, 0), fill='both', expand=True)

        # Campos da Licença Sanitária
        tk.Label(sanitaria_frame, text="Número da Licença *:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(5, 2))
        self.entry_licenca_sanitaria = tk.Entry(sanitaria_frame, width=35, font=('Arial', 10))
        self.entry_licenca_sanitaria.pack(pady=(0, 15))

        tk.Label(sanitaria_frame, text="Data de Emissão *:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(0, 2))
        self.entry_data_emissao_san = tk.Entry(sanitaria_frame, width=35, font=('Arial', 10))
        self.entry_data_emissao_san.pack(pady=(0, 15))
        self.entry_data_emissao_san.insert(0, "DD/MM/AAAA")

        tk.Label(sanitaria_frame, text="Data de Validade *:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(0, 2))
        self.entry_data_validade_san = tk.Entry(sanitaria_frame, width=35, font=('Arial', 10))
        self.entry_data_validade_san.pack(pady=(0, 15))
        self.entry_data_validade_san.insert(0, "DD/MM/AAAA")

        tk.Label(sanitaria_frame, text="Status:", 
                bg='#f0f0f0', font=('Arial', 10)).pack(anchor='w', pady=(0, 2))
        self.combo_status_san = ttk.Combobox(sanitaria_frame, values=['Ativo', 'Vencido', 'Pendente'], 
                                           width=32, state='readonly')
        self.combo_status_san.set('Ativo')
        self.combo_status_san.pack(pady=(0, 10))

        # Frame para botões centralizados
        botoes_frame = tk.Frame(center_frame, bg='#f0f0f0')
        botoes_frame.pack(pady=40)

        # Botão Finalizar Cadastro
        tk.Button(botoes_frame, text="FINALIZAR CADASTRO", command=self.finalizar_cadastro,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 width=25, height=2).pack(pady=5)

        # Botão Voltar
        tk.Button(botoes_frame, text="VOLTAR", command=self.voltar_tela_estudio,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'),
                 width=15, height=2).pack(pady=5)

        # Bind scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Centralizar o canvas horizontalmente
        def centralizar_canvas(event=None):
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            content_width = scrollable_frame.winfo_reqwidth()
            if content_width < canvas_width:
                x = (canvas_width - content_width) // 2
                canvas.create_window((x, 0), window=scrollable_frame, anchor="n")
            else:
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        canvas.bind('<Configure>', centralizar_canvas)
        self.root.after(100, centralizar_canvas)

    def validar_data(self, data_str):
        """Valida e converte string de data para datetime"""
        try:
            return datetime.strptime(data_str, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Data inválida: {data_str}. Use o formato DD/MM/AAAA")

    def finalizar_cadastro(self):
        """Finaliza o cadastro criando estúdio e alvarás"""
        try:
            # Validar campos de alvará
            alvara_func = self.entry_alvara_funcionamento.get().strip()
            data_emissao_func = self.entry_data_emissao_func.get().strip()
            data_validade_func = self.entry_data_validade_func.get().strip()
            status_func = self.combo_status_func.get()

            licenca_san = self.entry_licenca_sanitaria.get().strip()
            data_emissao_san = self.entry_data_emissao_san.get().strip()
            data_validade_san = self.entry_data_validade_san.get().strip()
            status_san = self.combo_status_san.get()

            # Validações
            if not all([alvara_func, data_emissao_func, data_validade_func, 
                       licenca_san, data_emissao_san, data_validade_san]):
                raise ValueError("Preencha todos os campos obrigatórios de alvará")

            if data_emissao_func == "DD/MM/AAAA" or data_validade_func == "DD/MM/AAAA" or \
               data_emissao_san == "DD/MM/AAAA" or data_validade_san == "DD/MM/AAAA":
                raise ValueError("Informe as datas válidas")

            # Validar formato das datas
            dt_emissao_func = self.validar_data(data_emissao_func)
            dt_validade_func = self.validar_data(data_validade_func)
            dt_emissao_san = self.validar_data(data_emissao_san)
            dt_validade_san = self.validar_data(data_validade_san)

            # Primeiro cadastra o estúdio
            self.id_estudio_cadastrado = self.estudio_dao.criar_estudio(self.dados_estudio)

            # Cadastra Alvará de Funcionamento
            alvara_funcionamento = Alvara(
                id_estudio=self.id_estudio_cadastrado,
                numero_alvara=alvara_func,
                tipo_alvara="Alvará de Funcionamento",
                data_emissao=dt_emissao_func,
                data_validade=dt_validade_func,
                status=status_func,
                descricao="Alvará de Funcionamento do Estúdio",
                documento_anexo=None
            )
            self.alvara_dao.criar(alvara_funcionamento)

            # Cadastra Licença Sanitária
            licenca_sanitaria = Alvara(
                id_estudio=self.id_estudio_cadastrado,
                numero_alvara=licenca_san,
                tipo_alvara="Licença Sanitária",
                data_emissao=dt_emissao_san,
                data_validade=dt_validade_san,
                status=status_san,
                descricao="Licença Sanitária do Estúdio",
                documento_anexo=None
            )
            self.alvara_dao.criar(licenca_sanitaria)

            messagebox.showinfo("Sucesso", 
                              f"Cadastro finalizado com sucesso!\n"
                              f"Estúdio ID: {self.id_estudio_cadastrado}\n"
                              f"Alvarás cadastrados com sucesso!")
            
            # Volta para tela inicial limpa
            self.voltar_tela_estudio()
            self.limpar_campos()

        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao finalizar cadastro: {str(e)}")

    def voltar_tela_estudio(self):
        """Volta para a tela de cadastro de estúdio"""
        # Limpa a tela atual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Recria a interface original
        self.criar_interface()

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        campos = [
            self.entry_nome, self.entry_cnpj, self.entry_email,
            self.entry_telefone, self.entry_cep, self.entry_rua,
            self.entry_numero, self.entry_bairro, self.entry_complemento,
            self.entry_login, self.entry_senha, self.entry_confirmar_senha,
            self.entry_foto_perfil
        ]
        
        for campo in campos:
            campo.delete(0, tk.END)
        
        self.text_descricao.delete("1.0", tk.END)
        self.combo_uf.set('')
        self.combo_cidade.set('')
        self.combo_tipo.set('')