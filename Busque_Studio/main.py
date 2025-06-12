# main.py - Launcher do Sistema BusqueStudios
from app_principal import AppPrincipal
import tkinter as tk
import traceback

def main():
    """Função principal para inicializar a aplicação"""
    print("=" * 60)
    print("INICIANDO BUSQUE STUDIOS")
    print("=" * 60)
    print("Verificando dependências...")
    
    try:
        # Teste de importações
        import tkinter
        print("✓ tkinter OK")
        
        import mysql.connector
        print("✓ mysql.connector OK")
        
        print("=" * 60)
        print("INICIANDO APLICAÇÃO")
        print("=" * 60)
        
        # Criar janela principal (root)
        root = tk.Tk()
        root.title("BusqueStudios")
        root.geometry("1x1")  # Janela muito pequena, será escondida
        root.withdraw()  # Esconde a janela principal imediatamente
        
        # Inicializar a aplicação de login
        app = AppPrincipal(root)
        
        # Iniciar o loop principal
        root.mainloop()
        
    except ImportError as e:
        print(f"✗ Erro de importação: {e}")
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"✗ Erro na aplicação: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()