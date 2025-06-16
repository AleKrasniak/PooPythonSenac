from app_principal import AppPrincipal
def main():
    """Função principal para iniciar o sistema"""
    try:
        print("Iniciando BusqueStudios...")
        app = AppPrincipal()
        app.executar()
    except Exception as e:
        print(f"Erro ao iniciar o sistema: {e}")

if __name__ == "__main__":
    main()



# ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
# ATENÇÃO PROFESSOOOOOOOOOR
# PARA O CÓDIGO RODAR É NECESSÁRIO INSTALAR AS SEGUINTES BIBLIOTECAS 
# pip install pillow
# pip install requests
# pip install mysql-connector-python
# ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
