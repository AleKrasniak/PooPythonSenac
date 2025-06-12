import tkinter as tk

def criar_botao_voltar(root, callback_voltar):
    """Cria botão Voltar no canto superior esquerdo da janela 'root'."""
    # Usar a mesma cor de fundo da janela pai
    bg_color = root.cget('bg') if hasattr(root, 'cget') else '#34495e'
    
    frame_voltar = tk.Frame(root, bg=bg_color)
    frame_voltar.pack(fill='x', pady=(10, 0))
    
    btn_voltar = tk.Button(
        frame_voltar, 
        text="← Voltar",
        command=lambda: _voltar(root, callback_voltar),
        bg='#95a5a6', fg='white',
        font=('Arial', 10, 'bold'),
        width=10, height=1,
        cursor='hand2',
        relief='flat',
        bd=0
    )
    btn_voltar.pack(side='left', padx=20, pady=5)

def _voltar(root, callback_voltar):
    """Função interna para chamar o callback sem destruir a janela."""
    if callback_voltar:
        callback_voltar()