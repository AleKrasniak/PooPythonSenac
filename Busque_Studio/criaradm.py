# verificar_admin_corrigido.py
# Script para verificar e criar admin na tabela ADMINISTRADOR

import mysql.connector

def verificar_admin_no_banco():
    """Verifica se o admin foi criado corretamente na tabela ADMINISTRADOR"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("🔍 VERIFICANDO ADMIN NA TABELA ADMINISTRADOR...")
        print("=" * 50)
        
        # Buscar todos os registros na tabela administrador
        cursor.execute("""
            SELECT id_administrador, id_perfil, nome, email, login, senha
            FROM administrador 
            WHERE nome LIKE '%admin%' 
            OR email LIKE '%admin%' 
            OR login LIKE '%admin%'
            OR login = 'adminale'
        """)
        
        admins = cursor.fetchall()
        
        if not admins:
            print("❌ NENHUM ADMIN ENCONTRADO NA TABELA ADMINISTRADOR!")
            print("Vamos verificar todos os registros...")
            
            cursor.execute("SELECT id_administrador, id_perfil, nome, email, login, senha FROM administrador")
            todos_admins = cursor.fetchall()
            
            print(f"\n📋 TODOS OS ADMINISTRADORES ({len(todos_admins)}):")
            if todos_admins:
                for admin in todos_admins:
                    print(f"   ID: {admin[0]} | Perfil: {admin[1]} | Nome: {admin[2]} | Email: {admin[3]} | Login: {admin[4]} | Senha: {admin[5]}")
            else:
                print("   ⚠️  Tabela administrador está vazia!")
        else:
            print(f"✅ ADMINS ENCONTRADOS ({len(admins)}):")
            for admin in admins:
                print(f"   ID: {admin[0]}")
                print(f"   Perfil: {admin[1]}")
                print(f"   Nome: {admin[2]}")
                print(f"   Email: {admin[3]}")
                print(f"   Login: '{admin[4]}'")  # Aspas para ver espaços
                print(f"   Senha: '{admin[5]}'")  # Aspas para ver espaços
                print("   " + "-" * 30)
        
        # Testar login específico na tabela administrador
        print("\n🔍 TESTANDO LOGIN ESPECÍFICO NA TABELA ADMINISTRADOR...")
        cursor.execute("SELECT * FROM administrador WHERE login = %s AND senha = %s", ('adminale', '123'))
        resultado_exato = cursor.fetchone()
        
        if resultado_exato:
            print("✅ Login 'adminale' + senha '123' ENCONTRADO!")
        else:
            print("❌ Login 'adminale' + senha '123' NÃO ENCONTRADO!")
            
            # Testar variações
            print("\n🔍 Testando variações...")
            
            # Com espaços
            cursor.execute("SELECT * FROM administrador WHERE TRIM(login) = %s AND TRIM(senha) = %s", ('adminale', '123'))
            if cursor.fetchone():
                print("⚠️  Encontrado com TRIM - há espaços extras!")
            
            # Case insensitive
            cursor.execute("SELECT * FROM administrador WHERE LOWER(login) = %s AND senha = %s", ('adminale', '123'))
            if cursor.fetchone():
                print("⚠️  Encontrado com LOWER - problema de case!")
            
            # Só login
            cursor.execute("SELECT login, senha FROM administrador WHERE login = %s", ('adminale',))
            resultado_login = cursor.fetchone()
            if resultado_login:
                print(f"⚠️  Login encontrado mas senha diferente: '{resultado_login[1]}'")
            
            # Só senha
            cursor.execute("SELECT login, senha FROM administrador WHERE senha = %s", ('123',))
            resultado_senha = cursor.fetchone()
            if resultado_senha:
                print(f"⚠️  Senha encontrada mas login diferente: '{resultado_senha[0]}'")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def testar_login_como_aplicacao():
    """Testa o login da mesma forma que a aplicação faria na tabela administrador"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n🧪 TESTANDO LOGIN COMO A APLICAÇÃO (TABELA ADMINISTRADOR)...")
        print("=" * 50)
        
        login_teste = 'adminale'
        senha_teste = '123'
        
        print(f"Tentando login: '{login_teste}' com senha: '{senha_teste}'")
        
        # Método 1: Busca exata
        cursor.execute("SELECT * FROM administrador WHERE login = %s AND senha = %s", (login_teste, senha_teste))
        resultado1 = cursor.fetchone()
        print(f"Método 1 (busca exata): {'✅ SUCESSO' if resultado1 else '❌ FALHOU'}")
        
        # Método 2: Com trim
        cursor.execute("SELECT * FROM administrador WHERE TRIM(login) = %s AND TRIM(senha) = %s", (login_teste, senha_teste))
        resultado2 = cursor.fetchone()
        print(f"Método 2 (com trim): {'✅ SUCESSO' if resultado2 else '❌ FALHOU'}")
        
        # Método 3: Case insensitive
        cursor.execute("SELECT * FROM administrador WHERE LOWER(TRIM(login)) = %s AND TRIM(senha) = %s", (login_teste.lower(), senha_teste))
        resultado3 = cursor.fetchone()
        print(f"Método 3 (case insensitive): {'✅ SUCESSO' if resultado3 else '❌ FALHOU'}")
        
        # Se encontrou algum resultado, mostrar
        if resultado1 or resultado2 or resultado3:
            resultado = resultado1 or resultado2 or resultado3
            print(f"\n✅ DADOS DO ADMINISTRADOR ENCONTRADO:")
            print(f"   ID: {resultado[0]}")
            print(f"   Perfil: {resultado[1]}")
            print(f"   Nome: {resultado[2]}")
            print(f"   Email: {resultado[3]}")
            print(f"   Login: {resultado[4]}")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

def criar_admin_na_tabela_administrador():
    """Cria admin na tabela ADMINISTRADOR de forma garantida"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n🔧 CRIANDO ADMIN NA TABELA ADMINISTRADOR...")
        print("=" * 50)
        
        # Remover qualquer admin existente
        cursor.execute("DELETE FROM administrador WHERE login = 'adminale' OR email = 'admin@busquestudios.com'")
        removidos = cursor.rowcount
        print(f"🗑️  Removidos {removidos} registros antigos")
        
        # Garantir que existe perfil admin (assumindo id_perfil = 3 para admin)
        cursor.execute("SELECT id_perfil FROM perfil WHERE id_perfil = 3")
        if not cursor.fetchone():
            print("⚠️  Criando perfil admin...")
            cursor.execute("INSERT INTO perfil (id_perfil, nome_perfil) VALUES (3, 'Admin')")
            conexao.commit()
        
        # Criar admin na tabela administrador
        cursor.execute("""
            INSERT INTO administrador (id_perfil, nome, email, login, senha)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            3,                          # id_perfil (admin)
            'Admin Sistema',            # nome
            'admin@busquestudios.com', # email
            'adminale',                # login (sem espaços)
            '123'                      # senha (sem espaços)
        ))
        
        conexao.commit()
        print("✅ Admin criado com sucesso na tabela ADMINISTRADOR!")
        
        # Verificar imediatamente
        cursor.execute("SELECT id_administrador, id_perfil, nome, login, senha FROM administrador WHERE login = 'adminale'")
        verificacao = cursor.fetchone()
        
        if verificacao:
            print("🎉 VERIFICAÇÃO IMEDIATA:")
            print(f"   ID Admin: {verificacao[0]}")
            print(f"   ID Perfil: {verificacao[1]}")
            print(f"   Nome: {verificacao[2]}")
            print(f"   Login: '{verificacao[3]}'")
            print(f"   Senha: '{verificacao[4]}'")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")

def verificar_estrutura_tabelas():
    """Verifica se as tabelas necessárias existem"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n📋 VERIFICANDO ESTRUTURA DAS TABELAS...")
        print("=" * 50)
        
        # Verificar tabela administrador
        cursor.execute("SHOW TABLES LIKE 'administrador'")
        if cursor.fetchone():
            print("✅ Tabela 'administrador' existe")
            
            # Mostrar estrutura
            cursor.execute("DESCRIBE administrador")
            colunas = cursor.fetchall()
            print("   Colunas:")
            for coluna in colunas:
                print(f"     - {coluna[0]} ({coluna[1]})")
        else:
            print("❌ Tabela 'administrador' NÃO existe!")
            print("   Você precisa criar a tabela primeiro!")
        
        # Verificar tabela perfil
        cursor.execute("SHOW TABLES LIKE 'perfil'")
        if cursor.fetchone():
            print("✅ Tabela 'perfil' existe")
        else:
            print("❌ Tabela 'perfil' NÃO existe!")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar estrutura: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO COMPLETO DE LOGIN - TABELA ADMINISTRADOR")
    print("=" * 70)
    
    # 0. Verificar estrutura das tabelas
    verificar_estrutura_tabelas()
    
    # 1. Verificar o que existe no banco
    verificar_admin_no_banco()
    
    # 2. Testar login
    testar_login_como_aplicacao()
    
    # 3. Perguntar se quer recriar
    print("\n" + "=" * 70)
    resposta = input("❓ Quer criar o admin na tabela ADMINISTRADOR? (s/n): ")
    
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        criar_admin_na_tabela_administrador()
        print("\n✨ Agora teste novamente o login!")
        print("   Login: adminale")
        print("   Senha: 123")
        print("\n🔧 O admin foi criado na tabela ADMINISTRADOR, não na tabela CLIENTE!")
    
    print("\n💡 DICA: Se ainda não funcionar, verifique se seu código de login")
    print("    está consultando a tabela 'administrador' e não 'cliente'!")