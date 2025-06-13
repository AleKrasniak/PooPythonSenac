# debug_admin_login.py
# Script para debugar e corrigir problema de login do admin

import mysql.connector

def verificar_admin_detalhado():
    """Verifica detalhadamente os dados do admin no banco"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("🔍 DEBUG DETALHADO DO ADMIN")
        print("=" * 50)
        
        # Verificar se existe admin
        cursor.execute("SELECT * FROM administrador WHERE login = 'adminale'")
        admin = cursor.fetchone()
        
        if admin:
            print("✅ Admin encontrado!")
            print(f"   ID: {admin[0]}")
            print(f"   ID Perfil: {admin[1]}")
            print(f"   Nome: {admin[2]}")
            print(f"   Email: {admin[3]}")
            print(f"   Login: {admin[4]}")
            print(f"   Senha armazenada: '{admin[5]}'")
            print(f"   Tipo da senha: {type(admin[5])}")
            print(f"   Comprimento da senha: {len(admin[5])}")
            
            # Verificar caracteres especiais
            senha_bytes = admin[5].encode('utf-8')
            print(f"   Senha em bytes: {senha_bytes}")
            
        else:
            print("❌ Admin não encontrado!")
            
            # Listar todos os admins
            cursor.execute("SELECT login, senha FROM administrador")
            todos_admins = cursor.fetchall()
            print(f"\n📋 Todos os admins no banco ({len(todos_admins)}):")
            for admin_item in todos_admins:
                print(f"   Login: '{admin_item[0]}', Senha: '{admin_item[1]}'")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def testar_login_variações():
    """Testa várias variações de login"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n🧪 TESTANDO VARIAÇÕES DE LOGIN")
        print("=" * 50)
        
        # Variações para testar
        testes = [
            ('adminale', '123'),
            ('adminale', ' 123'),
            ('adminale', '123 '),
            (' adminale', '123'),
            ('adminale ', '123'),
            ('ADMINALE', '123'),
            ('adminale', 'admin'),
            ('admin', '123')
        ]
        
        for login, senha in testes:
            cursor.execute("""
                SELECT id_administrador, nome 
                FROM administrador 
                WHERE login = %s AND senha = %s
            """, (login, senha))
            
            resultado = cursor.fetchone()
            status = "✅" if resultado else "❌"
            print(f"   {status} Login: '{login}' | Senha: '{senha}'")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def recriar_admin_limpo():
    """Recria o admin de forma limpa"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n🔧 RECRIANDO ADMIN LIMPO")
        print("=" * 50)
        
        # 1. Remover todos os admins existentes
        cursor.execute("DELETE FROM administrador")
        removidos = cursor.rowcount
        print(f"🗑️  Removidos {removidos} admins")
        
        # 2. Verificar/criar perfil administrador
        cursor.execute("SELECT id_perfil FROM perfil WHERE nome = 'Administrador'")
        perfil = cursor.fetchone()
        
        if not perfil:
            cursor.execute("""
                INSERT INTO perfil (nome, descricao) 
                VALUES ('Administrador', 'Perfil com acesso total')
            """)
            id_perfil = cursor.lastrowid
            print(f"✅ Perfil criado (ID: {id_perfil})")
        else:
            id_perfil = perfil[0]
            print(f"✅ Perfil existe (ID: {id_perfil})")
        
        # 3. Criar admin com dados bem simples
        cursor.execute("""
            INSERT INTO administrador (id_perfil, nome, email, login, senha)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            id_perfil,
            'Admin',
            'admin@teste.com',
            'admin',
            '123'
        ))
        
        id_novo_admin = cursor.lastrowid
        conexao.commit()
        
        print(f"✅ Novo admin criado (ID: {id_novo_admin})")
        print("📋 NOVOS DADOS:")
        print("   Login: admin")
        print("   Senha: 123")
        
        # 4. Teste imediato
        cursor.execute("""
            SELECT id_administrador, nome, login, senha
            FROM administrador 
            WHERE login = 'admin' AND senha = '123'
        """, )
        
        teste = cursor.fetchone()
        if teste:
            print("✅ TESTE DE LOGIN: SUCESSO!")
            print(f"   Dados encontrados: ID={teste[0]}, Nome='{teste[1]}'")
        else:
            print("❌ TESTE DE LOGIN: FALHOU!")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def verificar_estrutura_tabela():
    """Verifica a estrutura da tabela administrador"""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="busquestudios2"
        )
        cursor = conexao.cursor()
        
        print("\n📋 ESTRUTURA DA TABELA ADMINISTRADOR")
        print("=" * 50)
        
        cursor.execute("DESCRIBE administrador")
        campos = cursor.fetchall()
        
        for campo in campos:
            print(f"   {campo[0]}: {campo[1]} (Null: {campo[2]}, Key: {campo[3]}, Default: {campo[4]})")
        
        cursor.close()
        conexao.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def mostrar_codigo_flask():
    """Mostra código Flask correto para login"""
    print("\n💻 CÓDIGO FLASK PARA LOGIN")
    print("=" * 50)
    
    codigo_flask = '''
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login', '').strip()  # Remove espaços
    senha = data.get('senha', '').strip()  # Remove espaços
    
    try:
        cursor = mysql.connection.cursor()
        
        # Query exata (sem hash de senha)
        cursor.execute("""
            SELECT a.id_administrador, a.nome, a.email, p.nome as perfil
            FROM administrador a
            JOIN perfil p ON a.id_perfil = p.id_perfil
            WHERE a.login = %s AND a.senha = %s
        """, (login, senha))
        
        admin = cursor.fetchone()
        cursor.close()
        
        if admin:
            session['admin_id'] = admin[0]
            session['admin_nome'] = admin[1]
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso',
                'admin': {
                    'id': admin[0],
                    'nome': admin[1],
                    'email': admin[2],
                    'perfil': admin[3]
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Login ou senha incorretos'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro no servidor: {str(e)}'
        }), 500
'''
    print(codigo_flask)

if __name__ == "__main__":
    print("🚨 DEBUG DO PROBLEMA DE LOGIN")
    print("=" * 70)
    
    # 1. Verificar dados atuais
    verificar_admin_detalhado()
    
    # 2. Testar variações
    testar_login_variações()
    
    # 3. Verificar estrutura da tabela
    verificar_estrutura_tabela()
    
    # 4. Recriar admin limpo
    print("\n" + "="*50)
    resposta = input("Deseja recriar o admin? (s/n): ").lower()
    if resposta == 's':
        recriar_admin_limpo()
    
    # 5. Mostrar código Flask
    mostrar_codigo_flask()
    
    print("\n🎯 RESUMO PARA TESTE:")
    print("=" * 50)
    print("1. Execute este script")
    print("2. Use os dados: login='admin', senha='123'")
    print("3. Verifique se seu Flask remove espaços (.strip())")
    print("4. Confirme que está consultando a tabela 'administrador'")
    print("5. Teste no navegador ou Postman")