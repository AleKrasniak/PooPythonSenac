import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import mysql.connector
from clienteDAO import ClienteDAO
from estudioDAO import EstudioDAO
from enderecoDAO import EnderecoDAO

class ClienteDentro:
    def __init__(self, root, cliente_logado):
        self.root = root
        self.cliente_logado = cliente_logado
        self.cliente_dao = ClienteDAO()
        self.estudio_dao = EstudioDAO()
        self.endereco_dao = EnderecoDAO()
        
        self.root.title("BusqueStudios - Cliente")
        
        #tela cheia
        try:
            self.root.state('zoomed')  # Windows
        except:
            #tamanho padrão
            self.root.geometry("1200x800")
        
        # Define tamanho mínimo da janela
        self.root.minsize(800, 600)
        self.root.configure(bg='#f0f0f0')
        
        # Cria a interface de forma mais simples e direta
        self.criar_interface()
    
    def criar_interface(self):
        #janela
        self.frame_principal = tk.Frame(self.root, bg='#f0f0f0')
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        titulo = tk.Label(
            self.frame_principal, 
            text=f"Bem-vindo, {self.cliente_logado.get('nome', 'Cliente')}!", 
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        titulo.pack(pady=(0, 30))
        
        #botões principais
        self.frame_botoes = tk.Frame(self.frame_principal, bg='#f0f0f0')
        self.frame_botoes.pack(pady=20)
        
        #ver Perfil
        self.btn_ver_perfil = tk.Button(
            self.frame_botoes,
            text="Ver Perfil",
            command=self.ver_perfil,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=40,
            pady=15,
            cursor='hand2'
        )
        self.btn_ver_perfil.pack(side='left', padx=15)
        
        #buscar Estúdios
        self.btn_buscar_estudios = tk.Button(
            self.frame_botoes,
            text="Buscar Estúdios",
            command=self.buscar_estudios,
            font=('Arial', 14, 'bold'),
            bg='#2196F3',
            fg='white',
            padx=40,
            pady=15,
            cursor='hand2'
        )
        self.btn_buscar_estudios.pack(side='left', padx=15)
        
        #scroll para os estúdios
        self.criar_area_scroll()
        
        #atualização da interface
        self.root.update_idletasks()
    
    def criar_area_scroll(self):
        # Frame container para o scroll estidos
        self.scroll_container = tk.Frame(self.frame_principal, bg='#f0f0f0')
        self.scroll_container.pack(fill='both', expand=True, pady=(20, 0))
        
        # canva do scroll
        self.canvas = tk.Canvas(self.scroll_container, bg='#f0f0f0', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.scroll_container, orient="vertical", command=self.canvas.yview)
        
        # canva que dá scroll
        self.frame_estudios = tk.Frame(self.canvas, bg='#f0f0f0')
        
        # config scroll
        self.frame_estudios.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Posiciona o frame no canvas
        self.canvas.create_window((0, 0), window=self.frame_estudios, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack dos elementos
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind para scroll com mouse
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.frame_estudios.bind("<MouseWheel>", on_mousewheel)
    
    def ver_perfil(self):
        #popup desenvolimento
        messagebox.showinfo("Atenção","Função em Desenvolvimento")
    
    def obter_cidade_cliente(self):
        #cidade do cliente pelo endereco
        try:
            print("=== DEBUG: Iniciando busca da cidade ===")
            print(f"Cliente logado: {self.cliente_logado}")
            
            #id do cliente
            id_cliente = self.cliente_logado.get('id_cliente') or self.cliente_logado.get('id')
            print(f"ID do cliente: {id_cliente}")
            
            if not id_cliente:
                print("ID do cliente não encontrado")
                return None
                       
            cliente_completo = self.cliente_dao.buscar_por_id(id_cliente)
            print(f"Cliente completo: {cliente_completo}")
            
            if not cliente_completo:
                print(f"Cliente com ID {id_cliente} não encontrado no banco")
                return None
            
            # converte tupla para dicionário 
            if isinstance(cliente_completo, tuple):
                campos_cliente = ['id_cliente', 'id_endereco', 'id_tipo_cliente', 'nome', 'data_nascimento', 'genero', 'telefone', 'cpf', 'email', 'usuario', 'senha']
                
                if len(cliente_completo) >= len(campos_cliente):
                    cliente_dict = dict(zip(campos_cliente, cliente_completo))
                else:
                    print(f"Tupla tem {len(cliente_completo)} elementos, esperado pelo menos {len(campos_cliente)}")
                    return None
            elif isinstance(cliente_completo, dict):
                cliente_dict = cliente_completo
            else:
                print(f"Tipo de retorno não suportado: {type(cliente_completo)}")
                return None
            
            # id do endereço do cliente
            id_endereco = (cliente_dict.get('id_endereco') or 
                          cliente_dict.get('endereco_id') or 
                          self.cliente_logado.get('id_endereco'))
            print(f"ID do endereço: {id_endereco}")
            
            if not id_endereco:
                print(" Cliente não possui id_endereco cadastrado")
                return None
            
            #  dados do endereço
            print(f"Buscando endereço com ID {id_endereco}...")
            endereco = self.endereco_dao.buscar_por_id(id_endereco)
            print(f"Endereço encontrado: {endereco}")
            
            if not endereco:
                print(f" Endereço com ID {id_endereco} não encontrado")
                return None
            
            # tupla para dicionário 
            if isinstance(endereco, tuple):
                campos_endereco = ['id_endereco', 'rua', 'numero', 'bairro', 'cidade', 'uf', 'cep']
                
                if len(endereco) >= len(campos_endereco):
                    endereco_dict = dict(zip(campos_endereco, endereco))
                else:
                    print(f" Tupla de endereço tem {len(endereco)} elementos, esperado pelo menos {len(campos_endereco)}")
                    return None
            elif isinstance(endereco, dict):
                endereco_dict = endereco
            else:
                print(f" Tipo de retorno de endereço não suportado: {type(endereco)}")
                return None
            
            # return  cidade do endereço
            cidade = endereco_dict.get('cidade', '').strip() if endereco_dict.get('cidade') else ''
            print(f"Cidade extraída: '{cidade}'")
            
            if cidade:
                print(f"✅ Cidade encontrada: {cidade}")
                return cidade
            else:
                print("❌ Campo cidade vazio no endereço")
                return None
            
        except Exception as e:
            print(f"❌ Erro ao obter cidade do cliente: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def buscar_estudios(self):
        #Busca e exibe estúdios da mesma cidade do cliente
        try:
            # limpa o container de estúdios
            for widget in self.frame_estudios.winfo_children():
                widget.destroy()
            
            # pega a cidade do cliente logado
            cidade_cliente = self.obter_cidade_cliente()
            
            if not cidade_cliente:
                messagebox.showwarning("Aviso", 
                    "Não foi possível identificar sua cidade.\n\n" +
                    "Possíveis causas:\n" +
                    "• Você não possui endereço cadastrado\n" +
                    "• O campo cidade está vazio no seu endereço\n" +
                    "• Erro na conexão com o banco de dados\n\n" +
                    "Por favor, verifique seu perfil e endereço.")
                return
            
            # busca estudios na mesma cidade
            estudios = self.estudio_dao.listar_estudios()
            
            if not estudios:
                label_vazio = tk.Label(
                    self.frame_estudios,
                    text="Nenhum estúdio cadastrado no sistema",
                    font=('Arial', 16),
                    bg='#f0f0f0',
                    fg='#666'
                )
                label_vazio.pack(pady=50)
                return
            
            # filtra estúdios pela cidade
            estudios_na_cidade = []
            for estudio in estudios:
                estudio_cidade = estudio.get('cidade', '').strip()
                if estudio_cidade.lower() == cidade_cliente.lower():
                    estudios_na_cidade.append(estudio)
            
            if not estudios_na_cidade:
                # Se não encontrou, mostra todos os estúdios disponíveis
                label_info = tk.Label(
                    self.frame_estudios,
                    text=f"Nenhum estúdio encontrado em {cidade_cliente}.\nMostrando todos os estúdios disponíveis:",
                    font=('Arial', 14),
                    bg='#f0f0f0',
                    fg='#666'
                )
                label_info.pack(pady=30)
                
                for estudio in estudios:
                    self.criar_card_estudio(estudio)
                
                # atualiza a região de scroll
                self.canvas.update_idletasks()
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))
                return
            
            # mostrando estudios titulo
            titulo_secao = tk.Label(
                self.frame_estudios,
                text=f"Estúdios em {cidade_cliente} ({len(estudios_na_cidade)} encontrados)",
                font=('Arial', 18, 'bold'),
                bg='#f0f0f0',
                fg='#333'
            )
            titulo_secao.pack(pady=(0, 30))
            
            # estúdios resultado
            for estudio in estudios_na_cidade:
                self.criar_card_estudio(estudio)
            
            # atualiza a região de scroll
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar estúdios: {str(e)}")
            print(f"Erro detalhado: {e}")
            import traceback
            traceback.print_exc()
    
    def criar_card_estudio(self, estudio):
        #frame do card infos
        card_frame = tk.Frame(
            self.frame_estudios, 
            bg='white', 
            relief='solid', 
            bd=1
        )
        card_frame.pack(fill='x', padx=10, pady=10)
        
        #frame interno com padding
        inner_frame = tk.Frame(card_frame, bg='white')
        inner_frame.pack(fill='x', padx=15, pady=15)
        
        #foto e informações
        info_frame = tk.Frame(inner_frame, bg='white')
        info_frame.pack(fill='x')
        
        # carrega  a foto do estúdio
        self.carregar_foto_estudio(info_frame, estudio.get('foto_perfil'))
        
        #informações 
        texto_frame = tk.Frame(info_frame, bg='white')
        texto_frame.pack(side='left', fill='both', expand=True, padx=(15, 0))
        
        # Nome
        nome_label = tk.Label(
            texto_frame,
            text=estudio.get('nome', 'Nome não informado'),
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#333'
        )
        nome_label.pack(anchor='w')
        
        # tipo estúdio
        if estudio.get('tipo'):
            tipo_label = tk.Label(
                texto_frame,
                text=f"Tipo: {estudio.get('tipo')}",
                font=('Arial', 12),
                bg='white',
                fg='#666'
            )
            tipo_label.pack(anchor='w', pady=(3, 0))
        
        #endereço
        endereco_completo = self.formatar_endereco(estudio)
        endereco_label = tk.Label(
            texto_frame,
            text=endereco_completo,
            font=('Arial', 11),
            bg='white',
            fg='#666',
            wraplength=400
        )
        endereco_label.pack(anchor='w', pady=(3, 0))
        
        # descrição
        if estudio.get('descricao'):
            desc_text = estudio.get('descricao')[:150]
            if len(estudio.get('descricao', '')) > 150:
                desc_text += "..."
            
            desc_label = tk.Label(
                texto_frame,
                text=desc_text,
                font=('Arial', 10),
                bg='white',
                fg='#555',
                wraplength=400,
                justify='left'
            )
            desc_label.pack(anchor='w', pady=(8, 0))
        
        #botões
        botoes_frame = tk.Frame(texto_frame, bg='white')
        botoes_frame.pack(anchor='w', pady=(15, 0))
        
        #mais detalhes
        btn_detalhes = tk.Button(
            botoes_frame,
            text="Ver Detalhes",
            command=lambda e=estudio: self.ver_detalhes_estudio(e),
            font=('Arial', 10, 'bold'),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        btn_detalhes.pack(side='left', padx=(0, 10))
        
    
    def ver_detalhes_estudio(self, estudio):
        #descricao estudio
        detalhes = f"""📍 ESTÚDIO: {estudio.get('nome', 'N/A')}


🏢 Tipo: {estudio.get('tipo', 'Não informado')}

📍 Endereço Completo:
{self.formatar_endereco(estudio)}

📝 Descrição:
{estudio.get('descricao', 'Não informado')}
"""
        
        messagebox.showinfo("Detalhes do Estúdio", detalhes)
    
    def carregar_foto_estudio(self, parent_frame, foto_url):
        #foto estúdio
        try:
            if foto_url and foto_url.strip():
                # Tenta carregar a imagem da URL
                response = requests.get(foto_url.strip(), timeout=5)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    # Redimensiona a imagem mantendo proporção
                    image = image.resize((100, 100), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    # Label para a foto
                    foto_label = tk.Label(
                        parent_frame, 
                        image=photo, 
                        bg='white',
                        relief='solid',
                        bd=1
                    )
                    foto_label.image = photo  # Mantém referência
                    foto_label.pack(side='left')
                    return
        except Exception as e:
            print(f"Erro ao carregar foto: {e}")
        
        # se foto não conseguir carregar
        foto_padrao = tk.Label(
            parent_frame,
            text="📸\nSem\nFoto",
            font=('Arial', 9),
            bg='#e8e8e8',
            fg='#666',
            width=12,
            height=6,
            relief='solid',
            bd=1
        )
        foto_padrao.pack(side='left')
    
    def formatar_endereco(self, estudio):
        """Formata o endereço completo do estúdio"""
        endereco_partes = []
        
        if estudio.get('rua'):
            endereco_partes.append(estudio['rua'])
        
        if estudio.get('numero'):
            endereco_partes.append(f"nº {estudio['numero']}")
        
        if estudio.get('bairro'):
            endereco_partes.append(estudio['bairro'])
        
        if estudio.get('cidade'):
            endereco_partes.append(estudio['cidade'])
        
        if estudio.get('uf'):
            endereco_partes.append(estudio['uf'])
        
        return ", ".join(endereco_partes) if endereco_partes else "Endereço não informado"
