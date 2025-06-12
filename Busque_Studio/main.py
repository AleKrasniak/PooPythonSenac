# main.py - Launcher do Sistema BusqueStudios
from app_principal import AppPrincipal

def main():

    try:
        print("Iniciando BusqueStudios...")
        print("=" * 50)
        print("SISTEMA DE GESTÃO - BUSQUE STUDIOS")
        print("=" * 50)
        
        # Cria e executa a aplicação principal
        app = AppPrincipal()
        app.executar()
        
    except Exception as e:
        print(f"Erro ao iniciar o sistema: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()