import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
from cliente import Cliente
from clienteDAO import ClienteDAO
from endereco import Endereco
from enderecoDAO import EnderecoDAO

class AppCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Cliente - BusqueStudios")
        self.root.geometry("600x600")
        self.root.configure(bg='#f0f0f0')

        self.dao = ClienteDAO()
        self.endereco_dao = EnderecoDAO()
        self.perfil_id = 2  # ID para perfil de cliente
        self.perfil_nome = "Cliente"

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
        titulo = tk.Label(self.root, text="CADASTRO DE CLIENTE",
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        titulo.pack(pady=10)

        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(padx=20, pady=10, fill='x')

        # Campos de entrada
        campos = [
            ("Nome *:", "entry_nome"),
            ("Email *:", "entry_email"),
            ("CPF *:", "entry_cpf"),
            ("Telefone *:", "entry_telefone"),
            ("CEP * (12345-678):", "entry_cep"),
            ("Rua:", "entry_rua"),
            ("Número:", "entry_numero"),
            ("Bairro:", "entry_bairro"),
            ("Complemento:", "entry_complemento"),
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

        # Combobox para UF
        tk.Label(frame, text="UF *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        lista_uf = [uf['sigla'] for uf in self.estados]
        self.combo_uf = ttk.Combobox(frame, values=lista_uf, width=10, state='readonly')
        self.combo_uf.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        self.combo_uf.bind("<<ComboboxSelected>>", self.on_uf_selecionado)
        row += 1

        # Combobox para Cidade
        tk.Label(frame, text="Cidade *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_cidade = ttk.Combobox(frame, values=[], width=37, state='readonly')
        self.combo_cidade.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Combobox para Gênero
        tk.Label(frame, text="Gênero:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_genero = ttk.Combobox(frame, values=['Masculino', 'Feminino', 'Outro'], width=37, state='readonly')
        self.combo_genero.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Frame para botões
        frame_botoes = tk.Frame(self.root, bg='#f0f0f0')
        frame_botoes.pack(pady=20)

        # Botão de Cadastro
        btn_cadastrar = tk.Button(frame_botoes, text="CADASTRAR-SE COMO CLIENTE",
                                 command=self.criar, bg='#4CAF50', fg='white',
                                 font=('Arial', 12, 'bold'), width=25, height=2)
        btn_cadastrar.grid(row=0, column=0, padx=5)

        # Botão Limpar
        btn_limpar = tk.Button(frame_botoes, text="LIMPAR CAMPOS", command=self.limpar_campos,
                              bg='#607D8B', fg='white', font=('Arial', 10, 'bold'),
                              width=15, height=2)
        btn_limpar.grid(row=1, column=0, pady=10)

        # Botão Continuar
        btn_continuar = tk.Button(frame_botoes, text="CONTINUAR",
                                 command=self.continuar_para_dentro,
                                 bg='#2980b9', fg='white',
                                 font=('Arial', 12, 'bold'), width=25, height=2)
        btn_continuar.grid(row=2, column=0, pady=10)

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
            self.combo_cidade.set('')
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar cidades: {e}")
            self.combo_cidade['values'] = []
            self.combo_cidade.set('')

    def validar_cep(self, cep):
        cep = cep.strip()
        if len(cep) == 8 and cep.isdigit():
            return f"{cep[:5]}-{cep[5:]}"
        elif len(cep) == 9 and cep[5] == '-' and cep.replace('-', '').isdigit():
            return cep
        return None

    def criar(self):
        # Obter valores dos campos
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        cep = self.validar_cep(self.entry_cep.get())
        rua = self.entry_rua.get().strip()
        numero = self.entry_numero.get().strip()
        bairro = self.entry_bairro.get().strip()
        complemento = self.entry_complemento.get().strip()
        uf = self.combo_uf.get().strip()
        cidade = self.combo_cidade.get().strip()
        dt_nasc = self.entry_dt_nasc.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        genero = self.combo_genero.get().strip()

        # Validações básicas
        if not (nome and email and cpf and telefone and cep and uf and cidade):
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios (*)!")
            return

        if not cep:
            messagebox.showwarning("Atenção", "CEP inválido. Formato correto: 12345-678 ou 12345678")
            return

        try:
            # Criar endereço
            endereco = Endereco(
                rua=rua or "Não informado",
                numero=int(numero) if numero.isdigit() else 0,
                bairro=bairro or "Não informado",
                cidade=cidade,
                complemento=complemento or "Não informado",
                uf=uf,
                cep=cep,
                data_cadastro=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                data_atualizacao=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

            # Inserir endereço no banco
            id_endereco = self.endereco_dao.criar(endereco)
            if not id_endereco:
                raise Exception("Falha ao criar endereço: ID não foi gerado")

            # Criar cliente
            cliente = Cliente(
                id_perfil=self.perfil_id,
                id_endereco=id_endereco,
                nome=nome,
                dt_nasc=dt_nasc if dt_nasc else None,
                genero=genero if genero else None,
                telefone=telefone,
                cpf=cpf,
                email=email,
                login=login if login else None,
                senha=senha if senha else None
            )

            # Inserir cliente no banco
            self.dao.criar(cliente)
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.limpar_campos()

        except ValueError as ve:
            messagebox.showerror("Erro", f"Valor inválido: {ve}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar cliente: {str(e)}")

    def limpar_campos(self):
        campos = [
            self.entry_nome, self.entry_email, self.entry_cpf, self.entry_telefone,
            self.entry_cep, self.entry_rua, self.entry_numero, self.entry_bairro,
            self.entry_complemento, self.entry_dt_nasc, self.entry_login, self.entry_senha
        ]
        for campo in campos:
            campo.delete(0, tk.END)
        
        self.combo_uf.set('')
        self.combo_cidade.set('')
        self.combo_genero.set('')

    def continuar_para_dentro(self):
        # Verificar campos obrigatórios
        campos_obrigatorios = [
            (self.entry_nome.get().strip(), "Nome"),
            (self.entry_email.get().strip(), "Email"),
            (self.entry_cpf.get().strip(), "CPF"),
            (self.entry_telefone.get().strip(), "Telefone"),
            (self.combo_uf.get().strip(), "UF"),
            (self.combo_cidade.get().strip(), "Cidade")
        ]

        faltando = [nome for valor, nome in campos_obrigatorios if not valor]
        
        if faltando:
            messagebox.showwarning("Atenção", f"Preencha os campos obrigatórios: {', '.join(faltando)}")
            return
        
        # Aqui você pode adicionar a lógica para continuar
        messagebox.showinfo("Continuar", "Todos os campos obrigatórios estão preenchidos!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppCliente(root)
    root.mainloop()