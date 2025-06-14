import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from dao.estudio_dao import EstudioDAO
from models.estudio import Estudio

class AppEstudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Estúdio - BusqueStudios")
        self.root.geometry("750x750")
        self.root.configure(bg='#f0f0f0')

        self.estudio_dao = EstudioDAO()
        self.perfil_id = 3  # ID para perfil de estúdio
        self.perfil_nome = "Estúdio"

        self.criar_interface()

    def criar_interface(self):
        # Frame principal com scrollbar
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(main_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Título
        titulo = tk.Label(scrollable_frame, text="CADASTRO DE ESTÚDIO",
                         font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        titulo.pack(pady=10)

        # Frame para campos do formulário
        frame_campos = tk.Frame(scrollable_frame, bg='#f0f0f0')
        frame_campos.pack(pady=10, padx=20, fill='x')

        # Campos do formulário
        campos = [
            ("Nome do Estúdio *:", "entry_nome"),
            ("CNPJ * (somente números):", "entry_cnpj"),
            ("Email *:", "entry_email"),
            ("Telefone *:", "entry_telefone"),
            ("Descrição:", "text_descricao"),  # Text area para descrição
            ("CEP * (12345-678):", "entry_cep"),
            ("Rua:", "entry_rua"),
            ("Número:", "entry_numero"),
            ("Bairro:", "entry_bairro"),
            ("Complemento:", "entry_complemento"),
            ("Login *:", "entry_login"),
            ("Senha *:", "entry_senha", True),
            ("Confirme a Senha *:", "entry_confirmar_senha", True),
            ("URL da Foto de Perfil:", "entry_foto_perfil")
        ]

        row = 0
        for label, attr, *senha in campos:
            tk.Label(frame_campos, text=label, bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
            
            if attr == "text_descricao":
                # Área de texto para descrição
                text = tk.Text(frame_campos, width=40, height=4)
                text.grid(row=row, column=1, pady=3, padx=5)
                setattr(self, attr, text)
            else:
                # Campo de entrada normal
                entry = tk.Entry(frame_campos, width=40, show='*' if senha else '')
                entry.grid(row=row, column=1, pady=3, padx=5)
                setattr(self, attr, entry)
            
            row += 1

        # Combobox para UF
        tk.Label(frame_campos, text="UF *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_uf = ttk.Combobox(frame_campos, values=['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
                                                         'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                                                         'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'], 
                                    width=10, state='readonly')
        self.combo_uf.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Combobox para Cidade
        tk.Label(frame_campos, text="Cidade *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_cidade = ttk.Combobox(frame_campos, values=[], width=37, state='readonly')
        self.combo_cidade.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Combobox para Tipo de Estúdio
        tk.Label(frame_campos, text="Tipo de Estúdio *:", bg='#f0f0f0').grid(row=row, column=0, sticky='w', pady=3)
        self.combo_tipo = ttk.Combobox(frame_campos, 
                                      values=['Tatuagem', 'Fotografia', 'Música', 'Arte', 'Design', 'Áudio', 'Vídeo'], 
                                      width=37, state='readonly')
        self.combo_tipo.grid(row=row, column=1, sticky='w', pady=3, padx=5)
        row += 1

        # Botões
        frame_botoes = tk.Frame(scrollable_frame, bg='#f0f0f0')
        frame_botoes.pack(pady=20)

        btn_cadastrar = tk.Button(frame_botoes, text="CADASTRAR ESTÚDIO",
                                 command=self.criar_estudio,
                                 bg='#e74c3c', fg='white',
                                 font=('Arial', 12, 'bold'), 
                                 width=25, height=2)
        btn_cadastrar.grid(row=0, column=0, padx=5)

        btn_limpar = tk.Button(frame_botoes, text="LIMPAR CAMPOS", 
                              command=self.limpar_campos,
                              bg='#607D8B', fg='white', 
                              font=('Arial', 10, 'bold'),
                              width=15, height=2)
        btn_limpar.grid(row=1, column=0, pady=10)

    def validar_cep(self, cep):
        cep = cep.strip()
        if len(cep) == 8 and cep.isdigit():
            return f"{cep[:5]}-{cep[5:]}"
        elif len(cep) == 9 and cep[5] == '-' and cep.replace('-', '').isdigit():
            return cep
        return None

    def criar_estudio(self):
        try:
            # Obter valores dos campos
            nome = self.entry_nome.get().strip()
            cnpj = self.entry_cnpj.get().strip()
            email = self.entry_email.get().strip()
            telefone = self.entry_telefone.get().strip()
            descricao = self.text_descricao.get("1.0", tk.END).strip()
            cep = self.entry_cep.get().strip()
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

            # Validação de campos obrigatórios
            campos_obrigatorios = [
                (nome, "Nome do Estúdio"),
                (cnpj, "CNPJ"),
                (email, "Email"),
                (telefone, "Telefone"),
                (cep, "CEP"),
                (uf, "UF"),
                (cidade, "Cidade"),
                (tipo, "Tipo de Estúdio"),
                (login, "Login"),
                (senha, "Senha"),
                (confirmar_senha, "Confirmação de Senha")
            ]

            # Verifica campos vazios
            campos_faltando = [nome for valor, nome in campos_obrigatorios if not valor]
            if campos_faltando:
                messagebox.showwarning("Atenção", f"Preencha os campos obrigatórios:\n{', '.join(campos_faltando)}")
                return

            # Validação de CNPJ (14 dígitos)
            if len(cnpj) != 14 or not cnpj.isdigit():
                messagebox.showwarning("Atenção", "CNPJ inválido. Deve conter 14 dígitos numéricos.")
                return

            # Validação de CEP
            cep_formatado = self.validar_cep(cep)
            if not cep_formatado:
                messagebox.showwarning("Atenção", "CEP inválido. Formato correto: 12345-678 ou 12345678")
                return

            # Validação de senha
            if len(senha) < 6:
                messagebox.showwarning("Atenção", "A senha deve ter pelo menos 6 caracteres")
                return
                
            if senha != confirmar_senha:
                messagebox.showwarning("Atenção", "As senhas não coincidem")
                return

            # Verificar se login já existe
            if self.estudio_dao.buscar_por_login(login):
                messagebox.showwarning("Atenção", "Este login já está em uso. Escolha outro.")
                return

            # Criar objeto Estudio
            estudio = Estudio()
            estudio.id_perfil = self.perfil_id
            estudio.nome = nome
            estudio.cnpj = cnpj
            estudio.descricao = descricao
            estudio.login = login
            estudio.senha = senha
            estudio.tipo = tipo
            estudio.foto_perfil = foto_perfil if foto_perfil else None
            
            # Preparar dados do endereço
            estudio.endereco_data = {
                'rua': rua if rua else "Não informado",
                'numero': int(numero) if numero.isdigit() else 0,
                'bairro': bairro if bairro else "Não informado",
                'cidade': cidade,
                'complemento': complemento if complemento else "Não informado",
                'uf': uf,
                'cep': cep_formatado,
                'data_cadastro': datetime.now(),
                'data_atualizacao': datetime.now()
            }

            # Tentar cadastrar no banco de dados
            id_estudio = self.estudio_dao.criar(estudio)
            
            # Mensagem de sucesso com informações importantes
            mensagem_sucesso = f"""
            Estúdio cadastrado com sucesso!
            
            ID: {id_estudio}
            Nome: {nome}
            Login: {login}
            
            Anote estas informações para acesso futuro.
            """
            messagebox.showinfo("Sucesso", mensagem_sucesso)
            
            # Limpar campos após cadastro
            self.limpar_campos()

        except ValueError as ve:
            messagebox.showerror("Erro", f"Valor inválido em algum campo: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar estúdio:\n{str(e)}")

    def limpar_campos(self):
        # Limpar campos de entrada
        campos = [
            self.entry_nome, self.entry_cnpj, self.entry_email, 
            self.entry_telefone, self.entry_cep, self.entry_rua,
            self.entry_numero, self.entry_bairro, self.entry_complemento,
            self.entry_login, self.entry_senha, self.entry_confirmar_senha,
            self.entry_foto_perfil
        ]
        
        for campo in campos:
            campo.delete(0, tk.END)
        
        # Limpar área de texto
        self.text_descricao.delete("1.0", tk.END)
        
        # Limpar comboboxes
        self.combo_uf.set('')
        self.combo_cidade.set('')
        self.combo_tipo.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = AppEstudio(root)
    root.mainloop()