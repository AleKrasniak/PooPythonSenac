# verificar_login.py
# Script para verificar o que está acontecendo com o login

import mysql.connector

def verificar_admin_no_banco():
    """Verifica se o admin foi criado corretamente no banco"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("🔍 VERIFICANDO ADMIN NO BANCO...")
        print("=" * 50)
        
        # Buscar todos os registros que podem ser admin
        cursor.execute("""
            SELECT id_cliente, nome, email, login, senha, id_perfil
            FROM cliente 
            WHERE nome LIKE '%admin%' 
            OR email LIKE '%admin%' 
            OR login LIKE '%admin%'
            OR login = 'adminale'
        """)
        
        admins = cursor.fetchall()
        
        if not admins:
            print("❌ NENHUM ADMIN ENCONTRADO!")
            print("Vamos verificar todos os usuários...")
            
            cursor.execute("SELECT id_cliente, nome, email, login, senha FROM cliente")
            todos_usuarios = cursor.fetchall()
            
            print(f"\n📋 TODOS OS USUÁRIOS ({len(todos_usuarios)}):")
            for usuario in todos_usuarios:
                print(f"   ID: {usuario[0]} | Nome: {usuario[1]} | Email: {usuario[2]} | Login: {usuario[3]} | Senha: {usuario[4]}")
        else:
            print(f"✅ ADMINS ENCONTRADOS ({len(admins)}):")
            for admin in admins:
                print(f"   ID: {admin[0]}")
                print(f"   Nome: {admin[1]}")
                print(f"   Email: {admin[2]}")
                print(f"   Login: '{admin[3]}'")  # Aspas para ver espaços
                print(f"   Senha: '{admin[4]}'")  # Aspas para ver espaços
                print(f"   Perfil: {admin[5]}")
                print("   " + "-" * 30)
        
        # Testar login específico
        print("\n🔍 TESTANDO LOGIN ESPECÍFICO...")
        cursor.execute("SELECT * FROM cliente WHERE login = %s AND senha = %s", ('adminale', '123'))
        resultado_exato = cursor.fetchone()
        
        if resultado_exato:
            print("✅ Login 'adminale' + senha '123' ENCONTRADO!")
        else:
            print("❌ Login 'adminale' + senha '123' NÃO ENCONTRADO!")
            
            # Testar variações
            print("\n🔍 Testando variações...")
            
            # Com espaços
            cursor.execute("SELECT * FROM cliente WHERE TRIM(login) = %s AND TRIM(senha) = %s", ('adminale', '123'))
            if cursor.fetchone():
                print("⚠️  Encontrado com TRIM - há espaços extras!")
            
            # Case insensitive
            cursor.execute("SELECT * FROM cliente WHERE LOWER(login) = %s AND senha = %s", ('adminale', '123'))
            if cursor.fetchone():
                print("⚠️  Encontrado com LOWER - problema de case!")
            
            # Só login
            cursor.execute("SELECT login, senha FROM cliente WHERE login = %s", ('adminale',))
            resultado_login = cursor.fetchone()
            if resultado_login:
                print(f"⚠️  Login encontrado mas senha diferente: '{resultado_login[1]}'")
            
            # Só senha
            cursor.execute("SELECT login, senha FROM cliente WHERE senha = %s", ('123',))
            resultado_senha = cursor.fetchone()
            if resultado_senha:
                print(f"⚠️  Senha encontrada mas login diferente: '{resultado_senha[0]}'")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def testar_login_como_aplicacao():
    """Testa o login da mesma forma que a aplicação faria"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n🧪 TESTANDO LOGIN COMO A APLICAÇÃO...")
        print("=" * 50)
        
        login_teste = 'adminale'
        senha_teste = '123'
        
        print(f"Tentando login: '{login_teste}' com senha: '{senha_teste}'")
        
        # Método 1: Busca exata
        cursor.execute("SELECT * FROM cliente WHERE login = %s AND senha = %s", (login_teste, senha_teste))
        resultado1 = cursor.fetchone()
        print(f"Método 1 (busca exata): {'✅ SUCESSO' if resultado1 else '❌ FALHOU'}")
        
        # Método 2: Com trim
        cursor.execute("SELECT * FROM cliente WHERE TRIM(login) = %s AND TRIM(senha) = %s", (login_teste, senha_teste))
        resultado2 = cursor.fetchone()
        print(f"Método 2 (com trim): {'✅ SUCESSO' if resultado2 else '❌ FALHOU'}")
        
        # Método 3: Case insensitive
        cursor.execute("SELECT * FROM cliente WHERE LOWER(TRIM(login)) = %s AND TRIM(senha) = %s", (login_teste.lower(), senha_teste))
        resultado3 = cursor.fetchone()
        print(f"Método 3 (case insensitive): {'✅ SUCESSO' if resultado3 else '❌ FALHOU'}")
        
        # Se encontrou algum resultado, mostrar
        if resultado1 or resultado2 or resultado3:
            resultado = resultado1 or resultado2 or resultado3
            print(f"\n✅ DADOS DO USUÁRIO ENCONTRADO:")
            print(f"   ID: {resultado[0]}")
            print(f"   Nome: {resultado[2]}")  # Assumindo que nome está na posição 2
            print(f"   Perfil: {resultado[1]}")  # Assumindo que perfil está na posição 1
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

def criar_admin_garantido():
    """Cria admin de forma garantida, removendo qualquer existente"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n🔧 CRIANDO ADMIN GARANTIDO...")
        print("=" * 50)
        
        # Remover qualquer admin existente
        cursor.execute("DELETE FROM cliente WHERE login = 'adminale' OR email = 'admin@busquestudios.com'")
        removidos = cursor.rowcount
        print(f"🗑️  Removidos {removidos} registros antigos")
        
        # Garantir que existe endereço
        cursor.execute("SELECT id_endereco FROM endereco LIMIT 1")
        endereco = cursor.fetchone()
        
        if not endereco:
            cursor.execute("INSERT INTO endereco (rua, numero, bairro) VALUES ('Rua Admin', '100', 'Centro')")
            conexao.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            id_endereco = cursor.fetchone()[0]
        else:
            id_endereco = endereco[0]
        
        # Garantir que existe perfil admin
        cursor.execute("SELECT id_perfil FROM perfil WHERE id_perfil = 3")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO perfil (id_perfil, nome_perfil) VALUES (3, 'Admin')")
            conexao.commit()
        
        # Criar admin com dados limpos
        cursor.execute("""
            INSERT INTO cliente (id_perfil, id_endereco, nome, dt_nasc, genero, telefone, cpf, email, login, senha)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            3,                          # id_perfil
            id_endereco,                # id_endereco  
            'Admin Sistema',            # nome
            '1990-01-01',              # dt_nasc
            'M',                       # genero
            '41999999999',             # telefone
            '12345678900',             # cpf
            'admin@busquestudios.com', # email
            'adminale',                # login (sem espaços)
            '123'                      # senha (sem espaços)
        ))
        
        conexao.commit()
        print("✅ Admin criado com sucesso!")
        
        # Verificar imediatamente
        cursor.execute("SELECT id_cliente, nome, login, senha FROM cliente WHERE login = 'adminale'")
        verificacao = cursor.fetchone()
        
        if verificacao:
            print("🎉 VERIFICAÇÃO IMEDIATA:")
            print(f"   ID: {verificacao[0]}")
            print(f"   Nome: {verificacao[1]}")
            print(f"   Login: '{verificacao[2]}'")
            print(f"   Senha: '{verificacao[3]}'")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO COMPLETO DE LOGIN")
    print("=" * 60)
    
    # 1. Verificar o que existe no banco
    verificar_admin_no_banco()
    
    # 2. Testar login
    testar_login_como_aplicacao()
    
    # 3. Perguntar se quer recriar
    print("\n" + "=" * 60)
    resposta = input("❓ Quer recriar o admin de forma garantida? (s/n): ")
    
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        criar_admin_garantido()
        print("\n✨ Agora teste novamente o login!")
        print("   Login: adminale")
        print("   Senha: 123")
    
    print("\n🔧 Se ainda não funcionar, me mostre o código da sua tela de login!")