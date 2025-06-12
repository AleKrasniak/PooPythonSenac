# main.py - Launcher do Sistema BusqueStudios
from app_principal import AppPrincipal
import tkinter as tk
import traceback

def main():

    try:
        print("Iniciando BusqueStudios...")
        print("=" * 50)
        print("SISTEMA DE GESTÃO - BUSQUE STUDIOS")
        print("=" * 50)
        
        # Cria e executa a aplicação principal
        root = tk.Tk()
        app = AppPrincipal(root)  # Com o parâmetro parent


        root.mainloop()
        
    except Exception as e:
        print(f"\n{'='*50}")
        print("ERRO DETALHADO:")
        print(f"{'='*50}")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print(f"\nTraceback completo:")
        traceback.print_exc()
        print(f"{'='*50}")
        
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()