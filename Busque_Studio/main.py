# main.py - Diagnóstico de Importações
import sys
import os

def testar_importacoes():
    """Testa cada importação individualmente para identificar o problema"""
    
    print("=" * 60)
    print("DIAGNÓSTICO DO SISTEMA BUSQUE STUDIOS")
    print("=" * 60)
    
    # Lista de importações do app_principal.py
    importacoes = [
        ("tkinter", "import tkinter as tk"),
        ("tkinter.messagebox", "from tkinter import messagebox"),
        ("app_cliente", "from app_cliente import AppCliente"),
        ("app_estudio", "from app_estudio import AppEstudio"),
        ("app_admin", "from app_admin import AppAdmin"),
        ("clienteDAO", "from clienteDAO import ClienteDAO"),
        ("app_login", "from app_login import AppLogin"),
        ("botao_voltar", "from botao_voltar import criar_botao_voltar"),
        ("mysql.connector", "import mysql.connector"),
    ]
    
    erros_encontrados = []
    
    for nome, comando in importacoes:
        try:
            print(f"Testando {nome}... ", end="")
            exec(comando)
            print("✓ OK")
        except ImportError as e:
            print(f"✗ ERRO DE IMPORTAÇÃO: {e}")
            erros_encontrados.append((nome, f"ImportError: {e}"))
        except Exception as e:
            print(f"✗ ERRO: {e}")
            erros_encontrados.append((nome, f"{type(e).__name__}: {e}"))
    
    print("\n" + "=" * 60)
    
    if erros_encontrados:
        print("ERROS ENCONTRADOS:")
        print("=" * 60)
        for nome, erro in erros_encontrados:
            print(f"• {nome}: {erro}")
        
        print("\n" + "=" * 60)
        print("SOLUÇÕES SUGERIDAS:")
        print("=" * 60)
        
        for nome, erro in erros_encontrados:
            if "mysql.connector" in nome:
                print(f"• Para {nome}: Execute 'pip install mysql-connector-python'")
            elif any(x in nome for x in ["app_cliente", "app_estudio", "app_admin", "clienteDAO", "app_login", "botao_voltar"]):
                print(f"• Para {nome}: Verifique se o arquivo '{nome.replace('_', '')}.py' existe no mesmo diretório")
        
        return False
    else:
        print("TODAS AS IMPORTAÇÕES OK!")
        return True

def testar_conexao_banco():
    """Testa a conexão com o banco de dados"""
    print("\n" + "=" * 60)
    print("TESTANDO CONEXÃO COM BANCO DE DADOS")
    print("=" * 60)
    
    try:
        from clienteDAO import ClienteDAO
        print("Criando ClienteDAO... ", end="")
        dao = ClienteDAO()
        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ ERRO: {e}")
        print("\nPossíveis causas:")
        print("• Banco de dados não está rodando")
        print("• Credenciais incorretas")
        print("• Banco/tabelas não existem")
        return False

def main():
    print("Iniciando diagnóstico...")
    
    # Verifica arquivos necessários
    arquivos_necessarios = [
        "app_principal.py",
        "app_cliente.py", 
        "app_estudio.py",
        "app_admin.py",
        "clienteDAO.py",
        "app_login.py",
        "botao_voltar.py"
    ]
    
    print("\nVerificando arquivos...")
    arquivos_faltando = []
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✓ {arquivo}")
        else:
            print(f"✗ {arquivo} - ARQUIVO NÃO ENCONTRADO")
            arquivos_faltando.append(arquivo)
    
    if arquivos_faltando:
        print(f"\n⚠️  ARQUIVOS FALTANDO: {', '.join(arquivos_faltando)}")
        print("Coloque todos os arquivos no mesmo diretório do main.py")
        input("\nPressione Enter para continuar mesmo assim...")
    
    # Testa importações
    if testar_importacoes():
        # Se importações OK, testa banco
        if testar_conexao_banco():
            # Se tudo OK, tenta rodar o sistema
            print("\n" + "=" * 60)
            print("INICIANDO SISTEMA")
            print("=" * 60)
            
            try:
                import tkinter as tk
                from app_principal import AppPrincipal
                
                root = tk.Tk()
                app = AppPrincipal(root)
                root.mainloop()
                
            except Exception as e:
                print(f"Erro ao iniciar sistema: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("\n❌ Corrija os problemas de banco de dados antes de continuar")
    else:
        print("\n❌ Corrija os problemas de importação antes de continuar")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()