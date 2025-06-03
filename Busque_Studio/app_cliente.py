import tkinter as tk
from tkinter import ttk, messagebox
import requests
from cliente import Cliente
from clienteDAO import ClienteDAO

class AppCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Cliente - BusqueStudios")
        self.root.geometry("600x550")
        self.root.configure(bg='#f0f0f0')

        self.dao = ClienteDAO()
        self.perfil_id = 1  # Perfil fixo: Cliente
        self.perfil_nome = "Cliente"

        # Carrega UFs do IBGE
        self.estados = self.carregar_ufs()

        self.criar_interface()

    def carregar_ufs(self):
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

    def criar_interface(self):
        # Título
        titulo = tk.Label(self.root, text="CADASTRO DE CLIENTE",
                          font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        titulo.pack(pady=10)

        # Frame dos campos
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(padx=20, pady=10, fill='x')

        # Campos do formulário
        campos = [
            ("Nome *:", "entry_nome"),
            ("Email *:", "entry_email"),
            ("CPF *:", "entry_cpf"),
            ("Telefone *:", "entry_telefone"),
            ("Data Nasc (YYYY-MM-DD):", "entry_dt_nasc"),
            ("Login:", "entry_login"),
            ("Senha:", "entry_senha", True),
        ]

        row = 0
        for label, attr, *senha in campos:
            tk.Label(frame, text=label, bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
            entry = tk.Entry(frame, width=40, show='*' if senha else '')
            entry.grid(row=row, column=1, pady=3, padx=5)
            setattr(self, attr, entry)
            row += 1

        # Combo UF
        tk.Label(frame, text="UF *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        lista_uf = [uf['sigla'] for uf in self.estados]
        self.combo_uf = ttk.Combobox(frame, values=lista_uf, width=10, state='readonly')
        self.combo_uf.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        self.combo_uf.bind("<<ComboboxSelected>>", self.on_uf_selecionado)
        row += 1

        # Combo Cidade
        tk.Label(frame, text="Cidade *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_cidade = ttk.Combobox(frame, values=[], width=37, state='readonly')
        self.combo_cidade.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Combo Gênero
        tk.Label(frame, text="Gênero:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_genero = ttk.Combobox(frame, values=['M', 'F', 'Outro'], width=37, state='readonly')
        self.combo_genero.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Botões
        frame_botoes = tk.Frame(self.root, bg='#f0f0f0')
        frame_botoes.pack(pady=20)

        btn_cadastrar = tk.Button(frame_botoes, text="CADASTRAR-SE COMO CLIENTE",
                                  command=self.criar, bg='#4CAF50', fg='white',
                                  font=('Arial', 12, 'bold'), width=25, height=2)
        btn_cadastrar.grid(row=0, column=0, padx=5)

        btn_limpar = tk.Button(frame_botoes, text="LIMPAR CAMPOS", command=self.limpar_campos,
                               bg='#607D8B', fg='white', font=('Arial', 10, 'bold'),
                               width=15, height=2)
        btn_limpar.grid(row=1, column=0, pady=10)

    def on_uf_selecionado(self, event):
        uf = self.combo_uf.get()
        estado = next((e for e in self.estados if e['sigla'] == uf), None)
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
            self.combo_cidade.set('')  # limpa seleção anterior
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar cidades: {e}")
            self.combo_cidade['values'] = []
            self.combo_cidade.set('')

    def criar(self):
        # Validação dos campos obrigatórios
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        uf = self.combo_uf.get().strip()
        cidade = self.combo_cidade.get().strip()

        if not (nome and email and cpf and telefone and uf and cidade):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (*)!")
            return

        dt_nasc = self.entry_dt_nasc.get().strip() or None
        login = self.entry_login.get().strip() or None
        senha = self.entry_senha.get().strip() or None
        genero = self.combo_genero.get().strip() or None

        # Criar cliente (exemplo, ajuste conforme sua classe Cliente)
        cliente = Cliente(
            id_perfil=self.perfil_id,
            id_endereco=None,  # Aqui você pode integrar com o endereço real se quiser
            nome=nome,
            dt_nasc=dt_nasc,
            genero=genero,
            telefone=telefone,
            cpf=cpf,
            email=email,
            login=login,
            senha=senha,
            uf=uf,
            cidade=cidade
        )

        try:
            self.dao.criar(cliente)
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar cliente: {e}")

    def limpar_campos(self):
        campos = [
            self.entry_nome, self.entry_email, self.entry_cpf, self.entry_telefone,
            self.entry_dt_nasc, self.entry_login, self.entry_senha
        ]
        for campo in campos:
            campo.delete(0, tk.END)
        self.combo_uf.set('')
        self.combo_cidade.set('')
        self.combo_genero.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = AppCliente(root)
    root.mainloop()
