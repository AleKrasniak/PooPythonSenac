import tkinter as tk
from tkinter import messagebox
import sys
import traceback

# Definir debug_print ANTES de usar
def debug_print(msg):
    print(f"[DEBUG] {msg}")
    sys.stdout.flush()

# Inicializar variáveis
ClienteDAO = None
AppCliente = None
AppEstudio = None
AppAdmin = None
mysql = None

# Imports com tratamento de erro
try:
    debug_print("Importando ClienteDAO...")
    from clienteDAO import ClienteDAO
    debug_print("✓ ClienteDAO importado")
except ImportError as e:
    debug_print(f"✗ Erro ao importar ClienteDAO: {e}")
except Exception as e:
    debug_print(f"✗ Erro inesperado ao importar ClienteDAO: {e}")

try:
    debug_print("Importando botao_voltar...")
    from botao_voltar import criar_botao_voltar
    debug_print("✓ botao_voltar importado")
except ImportError as e:
    debug_print(f"✗ Erro ao importar botao_voltar: {e}")
    def criar_botao_voltar(janela, callback):
        # Versão simplificada caso não encontre o módulo
        frame = tk.Frame(janela, bg=janela.cget('bg'))
        frame.pack(fill='x', pady=(10, 0))
        btn = tk.Button(frame, text="← Voltar", command=callback,
                       bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'))
        btn.pack(side='left', padx=20)

try:
    debug_print("Importando módulos de aplicação...")
    from app_cliente import AppCliente
    debug_print("✓ AppCliente importado")
except ImportError as e:
    debug_print(f"✗ Erro ao importar AppCliente: {e}")
    AppCliente = None

try:
    from app_estudio import AppEstudio
    debug_print("✓ AppEstudio importado")
except ImportError as e:
    debug_print(f"✗ Erro ao importar AppEstudio: {e}")
    AppEstudio = None

try:
    from app_admin import AppAdmin
    debug_print("✓ AppAdmin importado")
except ImportError as e:
    debug_print(f"✗ Erro ao importar AppAdmin: {e}")
    AppAdmin = None

try:
    debug_print("Importando mysql.connector...")
    import mysql.connector
    debug_print("✓ mysql.connector importado")
except ImportError as e:
    debug_print(f"✗ Erro ao importar mysql.connector: {e}")
    mysql = None

class AppPrincipal:
    def __init__(self, parent):
        debug_print("Inicializando AppPrincipal...")
        self.parent = parent
        
        # Inicializar DAO com tratamento de erro
        try:
            if ClienteDAO:
                debug_print("Criando ClienteDAO...")
                self.dao = ClienteDAO()
                debug_print("✓ ClienteDAO criado")
            else:
                debug_print("⚠ ClienteDAO não disponível - modo demo")
                self.dao = None
        except Exception as e:
            debug_print(f"✗ Erro ao criar ClienteDAO: {e}")
            self.dao = None

        # Esconde janela principal ao abrir login
        self.parent.withdraw()
        debug_print("Janela principal escondida")

        debug_print("Criando janela de login...")
        self.janela = tk.Toplevel(parent)
        self.janela.title("BusqueStudios - Login")
        self.janela.geometry("600x500")
        self.janela.configure(bg='#34495e')
        self.janela.resizable(False, False)
        self.centralizar_janela()
        self.janela.transient(parent)
        self.janela.grab_set()

        debug_print("Criando interface...")
        self.criar_interface_login()

        # Ao fechar login, mostra a janela principal
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_login)
        debug_print("AppPrincipal inicializado com sucesso")

    def centralizar_janela(self):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (500 // 2)
        self.janela.geometry(f"600x500+{x}+{y}")

    def criar_interface_login(self):
        titulo = tk.Label(self.janela, text="FAZER LOGIN",
                          font=('Arial', 24, 'bold'),
                          bg='#34495e', fg='white')
        titulo.pack(pady=(40, 10))

        criar_botao_voltar(self.janela, self.fechar_login)

        frame_campos = tk.Frame(self.janela, bg='#34495e')
        frame_campos.pack(pady=30)

        tk.Label(frame_campos, text="Login:",
                 font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').grid(row=0, column=0, sticky='w', pady=15)

        self.entry_login = tk.Entry(frame_campos, width=30, font=('Arial', 14))
        self.entry_login.grid(row=0, column=1, pady=15, padx=(20, 0))

        tk.Label(frame_campos, text="Senha:",
                 font=('Arial', 14, 'bold'),
                 bg='#34495e', fg='white').grid(row=1, column=0, sticky='w', pady=15)

        self.entry_senha = tk.Entry(frame_campos, width=30, font=('Arial', 14), show='*')
        self.entry_senha.grid(row=1, column=1, pady=15, padx=(20, 0))

        frame_botoes = tk.Frame(self.janela, bg='#34495e')
        frame_botoes.pack(pady=50)

        btn_entrar = tk.Button(frame_botoes, text="ENTRAR",
                               command=self.fazer_login,
                               bg='#27ae60', fg='white',
                               font=('Arial', 14, 'bold'),
                               width=15, height=2,
                               cursor='hand2')
        btn_entrar.grid(row=0, column=0, padx=15)

        btn_cancelar = tk.Button(frame_botoes, text="CANCELAR",
                                command=self.fechar_login,
                                bg='#e74c3c', fg='white',
                                font=('Arial', 14, 'bold'),
                                width=15, height=2,
                                cursor='hand2')
        btn_cancelar.grid(row=0, column=1, padx=15)

        # Status para mostrar se está em modo demo
        if not self.dao:
            status = tk.Label(self.janela, text="MODO DEMO - Banco não conectado",
                            font=('Arial', 10), bg='#34495e', fg='#f39c12')
            status.pack(pady=10)

        self.entry_senha.bind('<Return>', lambda event: self.fazer_login())
        self.entry_login.bind('<Return>', lambda event: self.entry_senha.focus())

        self.entry_login.focus()

    def fazer_login(self):
        debug_print("Tentando fazer login...")
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha!", parent=self.janela)
            return

        try:
            if self.dao:
                debug_print("Validando credenciais no banco...")
                usuario = self.validar_credenciais(login, senha)
            else:
                debug_print("Modo demo - simulando login...")
                usuario = self.simular_login(login, senha)

            if usuario:
                debug_print(f"Login bem-sucedido: {usuario}")
                # Esconde a janela de login ao abrir perfil
                self.janela.withdraw()

                perfil = usuario['nome_perfil'].lower()
                debug_print(f"Abrindo perfil: {perfil}")

                # Abre a janela do perfil correto
                if perfil == 'admin' and AppAdmin:
                    janela_perfil = AppAdmin(self.janela)
                elif perfil == 'estúdio' and AppEstudio:
                    janela_perfil = AppEstudio(self.janela)
                elif AppCliente:
                    janela_perfil = AppCliente(self.janela)
                else:
                    debug_print("Nenhuma classe de perfil disponível - abrindo demo")
                    self.abrir_demo_perfil(usuario)
                    return

                # Quando a janela do perfil fechar, mostra a janela de login novamente
                janela_perfil.janela.protocol("WM_DELETE_WINDOW", lambda: self.voltar_ao_login(janela_perfil))

            else:
                messagebox.showerror("Erro", "Login ou senha incorretos!", parent=self.janela)
                self.limpar_campos()

        except Exception as e:
            debug_print(f"Erro no login: {e}")
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}", parent=self.janela)

    def simular_login(self, login, senha):
        """Simulação de login quando não há banco"""
        usuarios_demo = {
            ("admin", "123"): {"nome_perfil": "admin", "nome"
            : "Administrador Demo"},
            ("cliente", "123"): {"nome_perfil": "cliente", "nome": "Cliente Demo"},
            ("estudio", "123"): {"nome_perfil": "estúdio", "nome": "Estúdio Demo"}
        }
        
        return usuarios_demo.get((login, senha))

    def abrir_demo_perfil(self, usuario):
        """Abre uma janela demo quando as classes de perfil não estão disponíveis"""
        demo_window = tk.Toplevel(self.janela)
        demo_window.title(f"Demo - {usuario['nome_perfil']}")
        demo_window.geometry("400x300")
        demo_window.configure(bg='#34495e')
        
        tk.Label(demo_window, text=f"PERFIL: {usuario['nome_perfil'].upper()}",
                font=('Arial', 18, 'bold'), bg='#34495e', fg='white').pack(pady=30)
        
        tk.Label(demo_window, text=f"Usuário: {usuario['nome']}",
                font=('Arial', 14), bg='#34495e', fg='white').pack(pady=10)
        
        tk.Label(demo_window, text="Modo demonstração\n(Classes de perfil não encontradas)",
                font=('Arial', 12), bg='#34495e', fg='#f39c12').pack(pady=20)
        
        tk.Button(demo_window, text="VOLTAR", 
                 command=lambda: self.voltar_demo(demo_window),
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold')).pack(pady=20)

    def voltar_demo(self, demo_window):
        demo_window.destroy()
        self.janela.deiconify()

    def validar_credenciais(self, login, senha):
        if not self.dao or not self.dao.cursor:
            return None
            
        cursor = self.dao.cursor

        try:
            query = """
                SELECT c.id_cliente, c.nome, c.email, c.telefone, c.cpf, 
                       p.nome_perfil, c.id_perfil
                FROM cliente c
                INNER JOIN perfil p ON c.id_perfil = p.id_perfil
                WHERE c.login = %s AND c.senha = %s
            """
            cursor.execute(query, (login, senha))
            resultado = cursor.fetchone()

            if resultado:
                return {
                    'id_cliente': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'telefone': resultado[3],
                    'cpf': resultado[4],
                    'nome_perfil': resultado[5],
                    'id_perfil': resultado[6]
                }

            return None
        except Exception as e:
            debug_print(f"Erro na validação: {e}")
            raise e

    def limpar_campos(self):
        self.entry_login.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_login.focus()

    def voltar_ao_login(self, janela_perfil):
        """Fecha a janela do perfil e mostra novamente o login"""
        janela_perfil.janela.destroy()
        self.janela.deiconify()

    def fechar_login(self):
        """Ao fechar a janela login, encerra a aplicação"""
        debug_print("Fechando aplicação...")
        self.janela.destroy()
        self.parent.quit()

def main():
    """Função principal para inicializar a aplicação"""
    print("=" * 60)
    print("INICIANDO BUSQUE STUDIOS")
    print("=" * 60)
    print("Verificando dependências...")
    
    try:
        # Teste básico de tkinter
        debug_print("Testando tkinter...")
        import tkinter
        debug_print("✓ tkinter OK")
        
        debug_print("Verificando mysql.connector...")
        if mysql:
            debug_print("✓ mysql.connector OK")
        else:
            debug_print("⚠ mysql.connector não disponível")
        
        print("=" * 60)
        print("INICIANDO APLICAÇÃO")
        print("=" * 60)
        
        # Criar janela principal (root)
        debug_print("Criando janela root...")
        root = tk.Tk()
        root.title("BusqueStudios")
        root.geometry("1x1")  # Janela muito pequena, será escondida
        root.withdraw()  # Esconde a janela principal imediatamente
        debug_print("✓ Root criado e escondido")
        
        # Inicializar a aplicação de login
        debug_print("Inicializando AppPrincipal...")
        app = AppPrincipal(root)
        debug_print("✓ AppPrincipal inicializado")
        
        # Iniciar o loop principal
        debug_print("Iniciando mainloop...")
        root.mainloop()
        debug_print("Mainloop encerrado")
        
    except ImportError as e:
        print(f"✗ Erro de importação: {e}")
        traceback.print_exc()
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"✗ Erro na aplicação: {e}")
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()