import tkinter as tk 
from tkinter import messagebox
from usuarioDAO import UsuarioDAO
from usuario import Usuario

class App: 
    def __init__(self, root):
        self.dao = UsuarioDAO()
        self.root = root
        self.root.title("CRUD COM MySQL")
        self.root.geometry("400x400")


        # Campos
        #Nome
        self.label_nome = tk.Label(root, text="Nome")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(root)
        self.entry_nome.pack()

        #email
        self.label_email = tk.Label(root, text="Email")
        self.label_email.pack()
        self.entry_email = tk.Entry(root)
        self.entry_email.pack()

        #id
        self.label_id = tk.Label(root, text="ID (para atulizar/deletar)")
        self.label_id.pack()
        self.entry_id = tk.Entry(root)
        self.entry_id.pack()

        #botões
        tk.Button(root, text="Criar", command=self.criar).pack(pady=5)
        tk.Button(root, text="Listar", command=self.listar).pack(pady=5)
        tk.Button(root, text="Atualizar", command=self.atualizar).pack(pady=5)
        tk.Button(root, text="Deletar", command=self.deletar).pack(pady=5)

        self.text_resultado = tk.Text(root, height=10)
        self.text_resultado.pack()

    def criar(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        if nome and email:
            usuario = Usuario(nome=nome, email=email)
            self.dao.criar(usuario)
            messagebox.showinfo("SUCESSO!!!", "Usuário criado!")
            self.limpar_campos()
        else:
            messagebox.showwarning("Erro","Preencha todos os campos!")


    def listar(self):
        registros = self.dao.listar()
        self.text_resultado.delete("1.0" ,  tk.END) 
        for r in registros:
            self.text_resultado.insert(tk.END, f"ID:{r[0]} | Nome: {r[1]} | Email: {r[2]}\n ")

    def atualizar(self):
        id = self.entry_id.get()
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        if id and nome and email:
            usuario = Usuario(id=int(id), nome=nome, email=email)
            self.dao.atualizar(usuario)
            messagebox.showinfo("Atualizado", "Usuário atualizado!")
            self.limpar_campos()

        else: 
            messagebox.showwarning("Erro", "Preencha todos od campos e informe o ID")
    
    def deletar(self):
        id = self.entry_id.get()
        if id: 
            self.dao.deletar(int(id))
            messagebox.showinfo("Deletado", "Usuário se  fudeu!!")
            self.limpar_campos()
        
        else: 
            messagebox.showwearning("Error", "Informe o ID!")


    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_id.delete(0, tk.END)

    
#executável

if __name__=="__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()