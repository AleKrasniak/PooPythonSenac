import tkinter as tk
from tkinter import messagebox
import sys

def teste_tkinter():
    """Teste básico do tkinter"""
    try:
        root = tk.Tk()
        root.title("Teste BusqueStudios")
        root.geometry("400x300")
        root.configure(bg='#34495e')
        
        label = tk.Label(root, text="Tkinter funcionando!", 
                        font=('Arial', 16), 
                        bg='#34495e', fg='white')
        label.pack(pady=50)
        
        btn = tk.Button(root, text="OK", command=root.quit)
        btn.pack(pady=20)
        
        print("Janela criada com sucesso!")
        root.mainloop()
        return True
    except Exception as e:
        print(f"Erro no teste tkinter: {e}")
        return False

class LoginSimples:
    """Versão simplificada da tela de login"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BusqueStudios - Login Simples")
        self.root.geometry("600x500")
        self.root.configure(bg='#34495e')
        self.root.resizable(False, False)
        self.centralizar_janela()
        
        self.criar_interface()
        
    def centralizar_janela(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")

    def criar_interface(self):
        # Título
        titulo = tk.Label(self.root, text="BUSQUE STUDIOS - LOGIN",
                          font=('Arial', 24, 'bold'),
                          bg='#34495e', fg='white')
        titulo.pack(pady=(40, 30))

        # Frame para campos
        frame_campos = tk.Frame(self.root, bg='#34495e')
        frame_campos.pack(pady=30)

        # Campo Login
        tk.Label(frame_campos, text="Login:",
                 font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=15)

        self.entry_login = tk.Entry(frame_campos, width=30, font=('Arial', 14))
        self.entry_login.grid(row=0, column=1, pady=15, padx=(20, 0))

        # Campo Senha
        tk.Label(frame_campos, text="Senha:",
                 font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=15)

        self.entry_senha = tk.Entry(frame_campos, width=30, font=('Arial', 14), show='*')
        self.entry_senha.grid(row=1, column=1, pady=15, padx=(20, 0))

        # Frame para botões
        frame_botoes = tk.Frame(self.root, bg='#34495e')
        frame_botoes.pack(pady=50)

        btn_entrar = tk.Button(frame_botoes, text="ENTRAR",
                               command=self.fazer_login,
                               bg='#27ae60', fg='white',
                               font=('Arial', 14, 'bold'),
                               width=15, height=2,
                               cursor='hand2')
        btn_entrar.pack(side='left', padx=10)

        btn_sair = tk.Button(frame_botoes, text="SAIR",
                            command=self.sair,
                            bg='#e74c3c', fg='white',
                            font=('Arial', 14, 'bold'),
                            width=15, height=2,
                            cursor='hand2')
        btn_sair.pack(side='left', padx=10)

        # Bindings
        self.entry_senha.bind('<Return>', lambda event: self.fazer_login())
        self.entry_login.bind('<Return>', lambda event: self.entry_senha.focus())
        
        # Status
        self.status_label = tk.Label(self.root, text="Digite suas credenciais",
                                    font=('Arial', 12),
                                    bg='#34495e', fg='#bdc3c7')
        self.status_label.pack(pady=20)

        self.entry_login.focus()

    def fazer_login(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha!")
            return

        # Simulação de login (sem banco de dados)
        if login == "admin" and senha == "123":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.status_label.config(text="Login realizado com sucesso!", fg='#27ae60')
        elif login == "cliente" and senha == "123":
            messagebox.showinfo("Sucesso", "Login de cliente realizado!")
            self.status_label.config(text="Login de cliente realizado!", fg='#27ae60')
        elif login == "estudio" and senha == "123":
            messagebox.showinfo("Sucesso", "Login de estúdio realizado!")
            self.status_label.config(text="Login de estúdio realizado!", fg='#27ae60')
        else:
            messagebox.showerror("Erro", "Login ou senha incorretos!")
            self.status_label.config(text="Login ou senha incorretos!", fg='#e74c3c')
            self.limpar_campos()

    def limpar_campos(self):
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_login.focus()

    def sair(self):
        self.root.quit()

    def iniciar(self):
        print("Iniciando interface de login...")
        self.root.mainloop()

def main():
    print("=" * 60)
    print("TESTE BUSQUE STUDIOS")
    print("=" * 60)
    
    # Primeiro teste: verificar se tkinter funciona
    print("1. Testando tkinter básico...")
    # if not teste_tkinter():
    #     print("Erro: tkinter não está funcionando!")
    #     input("Pressione Enter para sair...")
    #     return
    
    print("2. Iniciando login simplificado...")
    
    try:
        app = LoginSimples()
        app.iniciar()
        print("Aplicação encerrada normalmente.")
        
    except Exception as e:
        print(f"Erro na aplicação: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()