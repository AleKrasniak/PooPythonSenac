import tkinter as tk

class TesteLogin:
    def __init__(self):
        print("[DEBUG] Iniciando TesteLogin...")
        self.root = tk.Tk()
        self.root.withdraw()  # Esconde a janela principal
        
        self.criar_janela_login()
        
    def criar_janela_login(self):
        print("[DEBUG] Criando janela de login...")
        
        self.janela_login = tk.Toplevel(self.root)
        print("[DEBUG] ✓ Toplevel criado")
        
        self.janela_login.title("Login - Teste")
        print("[DEBUG] ✓ Título definido")
        
        self.janela_login.geometry("400x300")
        print("[DEBUG] ✓ Geometria definida")
        
        # Adicione elementos um por vez
        label = tk.Label(self.janela_login, text="Login Teste")
        label.pack(pady=20)
        print("[DEBUG] ✓ Label criado")
        
        entry = tk.Entry(self.janela_login)
        entry.pack(pady=10)
        print("[DEBUG] ✓ Entry criado")
        
        button = tk.Button(self.janela_login, text="Teste", command=self.teste_comando)
        button.pack(pady=10)
        print("[DEBUG] ✓ Button criado")
        
        print("[DEBUG] Interface de login criada com sucesso")
        
    def teste_comando(self):
        print("[DEBUG] Botão clicado!")
        
    def iniciar(self):
        print("[DEBUG] Iniciando mainloop...")
        self.root.mainloop()

if __name__ == "__main__":
    app = TesteLogin()
    app.iniciar()