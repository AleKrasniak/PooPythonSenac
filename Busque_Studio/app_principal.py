import tkinter as tk
from tkinter import messagebox
from app_cliente import AppCliente
from app_estudio import AppEstudio
from app_admin import AppAdmin
from clienteDAO import ClienteDAO
from botao_voltar import criar_botao_voltar
import mysql.connector
import sys

class AppPrincipal:
    def __init__(self, parent):
        self.parent = parent
        self.dao = ClienteDAO()

        # Esconde janela principal ao abrir login
        self.parent.withdraw()

        self.janela = tk.Toplevel(parent)
        self.janela.title("BusqueStudios - Login")
        self.janela.geometry("600x500")
        self.janela.configure(bg='#34495e')
        self.janela.resizable(False, False)
        self.centralizar_janela()
        self.janela.transient(parent)
        self.janela.grab_set()

        self.criar_interface_login()

        # Ao fechar login, mostra a janela principal
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_login)

    def centralizar_janela(self):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (500 // 2)
        self.janela.geometry(f"600x500+{x}+{y}")

    def criar_interface_login(self):
        titulo = tk.Label(self.janela, text="FAZER LOGIN",
                          font=('Arial', 24, 'bold'),
                          bg='#34495e', fg='white')
        titulo.pack(pady=(40, 10))

        criar_botao_voltar(self.janela, self.fechar_login)

        frame_campos = tk.Frame(self.janela, bg='#34495e')
        frame_campos.pack(pady=30)

        tk.Label(frame_campos, text="Login:",
                 font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=15)

        self.entry_login = tk.Entry(frame_campos, width=30, font=('Arial', 14))
        self.entry_login.grid(row=0, column=1, pady=15, padx=(20, 0))

        tk.Label(frame_campos, text="Senha:",
                 font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=15)

        self.entry_senha = tk.Entry(frame_campos, width=30, font=('Arial', 14), show='*')
        self.entry_senha.grid(row=1, column=1, pady=15, padx=(20, 0))

        frame_botoes = tk.Frame(self.janela, bg='#34495e')
        frame_botoes.pack(pady=50)

        btn_entrar = tk.Button(frame_botoes, text="ENTRAR",
                               command=self.fazer_login,
                               bg='#27ae60', fg='white',
                               font=('Arial', 14, 'bold'),
                               width=15, height=2,
                               cursor='hand2')
        btn_entrar.grid(row=0, column=0, padx=15)

        btn_cancelar = tk.Button(frame_botoes, text="CANCELAR",
                                command=self.fechar_login,
                                bg='#e74c3c', fg='white',
                                font=('Arial', 14, 'bold'),
                                width=15, height=2,
                                cursor='hand2')
        btn_cancelar.grid(row=0, column=1, padx=15)

        self.entry_senha.bind('<Return>', lambda event: self.fazer_login())
        self.entry_login.bind('<Return>', lambda event: self.entry_senha.focus())

        self.entry_login.focus()

    def fazer_login(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha!", parent=self.janela)
            return

        try:
            usuario = self.validar_credenciais(login, senha)

            if usuario:
                # Esconde a janela de login ao abrir perfil
                self.janela.withdraw()

                perfil = usuario['nome_perfil'].lower()

                # Abre a janela do perfil correto
                if perfil == 'admin':
                    janela_perfil = AppAdmin(self.janela)
                elif perfil == 'estúdio':
                    janela_perfil = AppEstudio(self.janela)
                else:
                    janela_perfil = AppCliente(self.janela)

                # Quando a janela do perfil fechar, mostra a janela de login novamente
                janela_perfil.janela.protocol("WM_DELETE_WINDOW", lambda: self.voltar_ao_login(janela_perfil))

            else:
                messagebox.showerror("Erro", "Login ou senha incorretos!", parent=self.janela)
                self.limpar_campos()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}", parent=self.janela)

    def validar_credenciais(self, login, senha):
        cursor = self.dao.cursor

        try:
            query = """
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, 
                       p.nome_perfil, c.id_perfil
                FROM cliente c
                INNER JOIN perfil p ON c.id_perfil = p.id_perfil
                WHERE c.login = %s AND c.senha = %s
            """
            cursor.execute(query, (login, senha))
            resultado = cursor.fetchone()

            if resultado:
                return {
                    'id_cliente': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'telefone': resultado[3],
                    'cpf': resultado[4],
                    'nome_perfil': resultado[5],
                    'id_perfil': resultado[6]
                }

            return None
        except Exception as e:
            print(f"Erro na validação: {e}")
            raise e

    def limpar_campos(self):
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_login.focus()

    def voltar_ao_login(self, janela_perfil):
        """Fecha a janela do perfil e mostra novamente o login"""
        janela_perfil.janela.destroy()
        self.janela.deiconify()

    def fechar_login(self):
        """Ao fechar a janela login, encerra a aplicação"""
        self.janela.destroy()
        self.parent.quit()  # Mudança aqui: usar quit() ao invés de deiconify()