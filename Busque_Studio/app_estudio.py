import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from estudioDAO import EstudioDAO
from typing import Optional

class AppEstudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Estúdio - BusqueStudios")
        self.root.state('zoomed')  # Abre em tela cheia no Windows
        # Para sistemas Unix/Linux, use: self.root.attributes('-zoomed', True)
        self.root.configure(bg='#f0f0f0')

        self.estudio_dao = EstudioDAO()
        self.perfil_id = 3
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

        # Botão de Cadastro
        tk.Button(frame_botoes, text="CADASTRAR", command=self.cadastrar_estudio,
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

    def cadastrar_estudio(self):
        """Realiza o cadastro de um novo estúdio"""
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
            estudio_data = {
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

            # Cadastra no banco de dados
            id_estudio = self.estudio_dao.criar_estudio(estudio_data)
            messagebox.showinfo("Sucesso", f"Estúdio cadastrado com ID: {id_estudio}")
            self.limpar_campos()

        except ValueError as ve:
            messagebox.showerror("Erro de Validação", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {str(e)}")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = AppEstudio(root)
    root.mainloop()