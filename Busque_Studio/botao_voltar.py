import tkinter as tk

def criar_botao_voltar(root, callback_voltar):
    """Cria botão Voltar no canto superior esquerdo da janela 'root'."""
    frame_voltar = tk.Frame(root, bg='#f0f0f0')
    frame_voltar.pack(fill='x', pady=(10, 0))
    
    btn_voltar = tk.Button(
        frame_voltar, 
        text="← Voltar",
        command=lambda: _voltar(root, callback_voltar),
        bg='#95a5a6', fg='white',
        font=('Arial', 10, 'bold'),
        width=10, height=1,
        cursor='hand2'
    )
    btn_voltar.pack(side='left', padx=20, pady=5)

def _voltar(root, callback_voltar):
    """Função interna para fechar a janela atual e chamar o callback."""
    root.destroy()
    if callback_voltar:
        callback_voltar()