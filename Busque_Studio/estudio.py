import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import Dict, List, Optional

from datetime import datetime
from typing import Dict, Optional

class Estudio:
    def __init__(self, id_estudio: Optional[int] = None, 
                 id_perfil: Optional[int] = None, 
                 nome: str = "", 
                 cnpj: str = "", 
                 descricao: str = "", 
                 login: str = "", 
                 senha: str = "", 
                 tipo: str = "", 
                 email: str = "",
                 telefone: str = "",
                 foto_perfil: str = "",
                 endereco_data: Optional[Dict] = None):
        
        self.id_estudio = id_estudio
        self.id_perfil = id_perfil
        self.nome = nome
        self.cnpj = cnpj
        self.descricao = descricao
        self.login = login
        self.senha = senha
        self.tipo = tipo
        self.email = email
        self.telefone = telefone
        self.foto_perfil = foto_perfil
        self.endereco_data = endereco_data or {
            'rua': '',
            'numero': 0,
            'bairro': '',
            'cidade': '',
            'complemento': '',
            'uf': '',
            'cep': '',
            'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_atualizacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def validar(self) -> bool:
        campos_obrigatorios = [
            self.nome,
            self.cnpj,
            self.login,
            self.senha,
            self.tipo,
            self.email,
            self.telefone,
            self.endereco_data.get('cidade'),
            self.endereco_data.get('uf'),
            self.endereco_data.get('cep')
        ]
        
        if not all(campos_obrigatorios):
            return False
            
        if len(self.cnpj) != 14 or not self.cnpj.isdigit():
            return False
            
        if len(self.senha) < 6:
            return False
            
        return True


class EstudioDAOMock:
    """Classe mock para simular operações de banco de dados com estúdios"""
    
    def __init__(self):
        self.estudios = []
        self.next_id = 1

    def criar(self, estudio: Estudio) -> int:
        """Cria um novo estúdio na lista mock"""
        if not estudio.validar():
            raise ValueError("Dados do estúdio inválidos")
            
        # Verifica se CNPJ já existe
        if any(e.cnpj == estudio.cnpj for e in self.estudios):
            raise ValueError("CNPJ já cadastrado")
            
        # Verifica se login já existe
        if any(e.login == estudio.login for e in self.estudios):
            raise ValueError("Login já em uso")
        
        estudio.id_estudio = self.next_id
        self.next_id += 1
        self.estudios.append(estudio)
        return estudio.id_estudio

    def buscar_por_id(self, id_estudio: int) -> Optional[Estudio]:
        """Busca um estúdio pelo ID"""
        for estudio in self.estudios:
            if estudio.id_estudio == id_estudio:
                return estudio
        return None

    def buscar_por_login(self, login: str) -> Optional[Estudio]:
        """Busca um estúdio pelo login"""
        for estudio in self.estudios:
            if estudio.login == login:
                return estudio
        return None

    def listar_todos(self) -> List[Estudio]:
        """Lista todos os estúdios cadastrados"""
        return self.estudios.copy()

    def atualizar(self, estudio: Estudio) -> bool:
        """Atualiza os dados de um estúdio"""
        if not estudio.validar():
            return False
            
        for i, e in enumerate(self.estudios):
            if e.id_estudio == estudio.id_estudio:
                self.estudios[i] = estudio
                return True
        return False

    def deletar(self, id_estudio: int) -> bool:
        """Remove um estúdio"""
        for i, estudio in enumerate(self.estudios):
            if estudio.id_estudio == id_estudio:
                del self.estudios[i]
                return True
        return False


class AppEstudioCadastro(tk.Tk):
    """Interface gráfica para cadastro de estúdios (usando mock)"""
    
    def __init__(self):
        super().__init__()
        self.title("Cadastro de Estúdios - Mock")
        self.geometry("600x700")
        
        self.dao = EstudioDAOMock()
        self.criar_widgets()
        
    def criar_widgets(self):
        """Cria os componentes da interface"""
        tk.Label(self, text="Cadastro de Estúdio", font=("Arial", 16)).pack(pady=10)
        
        # Frame principal
        frame = tk.Frame(self)
        frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Campos do formulário
        campos = [
            ("Nome do Estúdio:", "nome"),
            ("CNPJ (14 dígitos):", "cnpj"),
            ("Descrição:", "descricao"),
            ("Login:", "login"),
            ("Senha:", "senha", True),
            ("Tipo:", "tipo"),
            ("Rua:", "rua"),
            ("Número:", "numero"),
            ("Bairro:", "bairro"),
            ("Cidade:", "cidade"),
            ("UF:", "uf"),
            ("CEP:", "cep"),
            ("Complemento:", "complemento")
        ]
        
        self.entries = {}
        for i, (label, field, *opts) in enumerate(campos):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame, show="*" if opts else "", width=30)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            self.entries[field] = entry
        
        # Botões
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Cadastrar", command=self.cadastrar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Limpar", command=self.limpar).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Listar", command=self.listar).pack(side="left", padx=10)
    
    def cadastrar(self):
        """Cadastra um novo estúdio"""
        try:
            # Cria objeto Estudio com os dados do formulário
            estudio = Estudio(
                nome=self.entries["nome"].get(),
                cnpj=self.entries["cnpj"].get(),
                descricao=self.entries["descricao"].get(),
                login=self.entries["login"].get(),
                senha=self.entries["senha"].get(),
                tipo=self.entries["tipo"].get(),
                endereco_data={
                    'rua': self.entries["rua"].get(),
                    'numero': self.entries["numero"].get(),
                    'bairro': self.entries["bairro"].get(),
                    'cidade': self.entries["cidade"].get(),
                    'uf': self.entries["uf"].get(),
                    'cep': self.entries["cep"].get(),
                    'complemento': self.entries["complemento"].get()
                }
            )
            
            # Tenta cadastrar
            id_estudio = self.dao.criar(estudio)
            messagebox.showinfo("Sucesso", f"Estúdio cadastrado com ID: {id_estudio}")
            self.limpar()
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {str(e)}")
    
    def limpar(self):
        """Limpa todos os campos do formulário"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def listar(self):
        """Lista todos os estúdios cadastrados"""
        estudios = self.dao.listar_todos()
        if not estudios:
            messagebox.showinfo("Lista", "Nenhum estúdio cadastrado")
            return
            
        lista = "\n".join(str(e) for e in estudios)
        messagebox.showinfo("Estúdios Cadastrados", lista)


if __name__ == "__main__":
    app = AppEstudioCadastro()
    app.mainloop()