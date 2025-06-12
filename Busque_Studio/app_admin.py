import tkinter as tk
from tkinter import messagebox, ttk
from clienteDAO import ClienteDAO
from botao_voltar import criar_botao_voltar  # <- IMPORTAÇÃO CERTA

class AppAdmin:
    """Janela do painel de administrador"""
    def __init__(self, parent):
        self.parent = parent
        # Esconde a janela pai ao abrir o admin
        self.parent.withdraw()

        self.janela = tk.Toplevel(parent)
        self.janela.title("Painel do Administrador")
        self.janela.geometry("800x600")
        self.janela.configure(bg="#2c3e50")
        self.janela.resizable(False, False)

        self.dao = ClienteDAO()

        # Centralizar e tornar modal
        self.centralizar_janela()
        self.janela.transient(parent)
        self.janela.grab_set()

        self.criar_interface_admin()

        # Quando fechar a janela admin, reexibe a janela anterior
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_e_voltar)

    def centralizar_janela(self):
        """Centraliza a janela"""
        self.janela.update_idletasks()
        largura = 800
        altura = 600
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def criar_interface_admin(self):
        """Cria a interface gráfica do painel do admin"""
        # Título
        titulo = tk.Label(self.janela, text="PAINEL DO ADMINISTRADOR", 
                          font=("Arial", 22, "bold"),
                          bg="#2c3e50", fg="white")
        titulo.pack(pady=30)

        # Botão Voltar que fecha a janela admin e mostra a anterior
        criar_botao_voltar(self.janela, self.fechar_e_voltar)

        # Tabela de clientes
        frame_tabela = tk.Frame(self.janela, bg="#2c3e50")
        frame_tabela.pack(pady=20)

        colunas = ("ID", "Nome", "Email", "Telefone", "CPF", "Perfil")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=110, anchor="center")

        self.tabela.pack(side=tk.LEFT)

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.carregar_clientes()

    def carregar_clientes(self):
        """Carrega dados da tabela cliente"""
        try:
            cursor = self.dao.cursor
            query = """
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, p.nome_perfil
                FROM cliente c
                INNER JOIN perfil p ON c.id_perfil = p.id_perfil
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            self.tabela.delete(*self.tabela.get_children())  # Limpa a tabela

            for linha in resultados:
                self.tabela.insert("", "end", values=linha)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar clientes: {str(e)}", parent=self.janela)

    def fechar_e_voltar(self):
        """Fecha esta janela e reexibe a janela anterior"""
        self.janela.destroy()
        self.parent.deiconify()
