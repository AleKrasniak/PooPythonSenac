import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from estudiodao import EstudioDAO
from typing import Optional

class AppEstudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Estúdio - BusqueStudios")
        self.root.geometry("750x750")
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
        # Frame principal com scrollbar
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Título
        tk.Label(scrollable_frame, text="CADASTRO DE ESTÚDIO", font=('Arial', 16, 'bold'), 
                bg='#f0f0f0', fg='#333').pack(pady=10)

        # Campos do formulário
        frame_campos = tk.Frame(scrollable_frame, bg='#f0f0f0')
        frame_campos.pack(pady=10, padx=20, fill='x')

        campos = [
            ("Nome do Estúdio *:", "entry_nome"),
            ("CNPJ * (14 dígitos):", "entry_cnpj"),
            ("Email *:", "entry_email"),
            ("Telefone *:", "entry_telefone"),
            ("Descrição:", "text_descricao"),
            ("CEP * (12345-678):", "entry_cep"),
            ("Rua:", "entry_rua"),
            ("Número:", "entry_numero"),
            ("Bairro:", "entry_bairro"),
            ("Complemento:", "entry_complemento"),
            ("Login *:", "entry_login"),
            ("Senha *:", "entry_senha", True),
            ("Confirme a Senha *:", "entry_confirmar_senha", True),
            ("URL da Foto:", "entry_foto_perfil")
        ]

        row = 0
        for label, attr, *senha in campos:
            tk.Label(frame_campos, text=label, bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
            
            if attr == "text_descricao":
                text = tk.Text(frame_campos, width=40, height=4)
                text.grid(row=row, column=1, pady=3, padx=5)
                setattr(self, attr, text)
            else:
                entry = tk.Entry(frame_campos, width=40, show='*' if senha else '')
                entry.grid(row=row, column=1, pady=3, padx=5)
                setattr(self, attr, entry)
            
            row += 1

        # Combobox para UF
        tk.Label(frame_campos, text="UF *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_uf = ttk.Combobox(frame_campos, values=[e['sigla'] for e in self.estados], 
                                    width=10, state='readonly')
        self.combo_uf.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        self.combo_uf.bind("<<ComboboxSelected>>", self.on_uf_selecionado)
        row += 1

        # Combobox para Cidade
        tk.Label(frame_campos, text="Cidade *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_cidade = ttk.Combobox(frame_campos, values=[], width=37, state='readonly')
        self.combo_cidade.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Combobox para Tipo
        tk.Label(frame_campos, text="Tipo *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_tipo = ttk.Combobox(frame_campos, 
                                     values=['Tatuagem', 'Fotografia', 'Música', 'Arte', 'Design', 'Áudio', 'Vídeo'], 
                                     width=37, state='readonly')
        self.combo_tipo.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Botões
        frame_botoes = tk.Frame(scrollable_frame, bg='#f0f0f0')
        frame_botoes.pack(pady=20)

        tk.Button(frame_botoes, text="CADASTRAR", command=self.cadastrar_estudio,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'), 
                 width=25, height=2).grid(row=0, column=0, padx=5)

        tk.Button(frame_botoes, text="LIMPAR", command=self.limpar_campos,
                 bg='#607D8B', fg='white', font=('Arial', 10, 'bold'),
                 width=15, height=2).grid(row=1, column=0, pady=10)

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