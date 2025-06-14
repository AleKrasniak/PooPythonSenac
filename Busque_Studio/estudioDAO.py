import mysql.connector
from datetime import datetime
from mysql.connector import Error

class EstudioDAO:
    def __init__(self):
        """Inicializa a conexão com o banco de dados"""
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="busquestudios2"
            )
            self.cursor = self.conexao.cursor(dictionary=True)  # Retorna resultados como dicionários
        except Error as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def criar(self, estudio):
        """Cria um novo estúdio no banco de dados"""
        try:
            # Verifica se o objeto estudio tem o atributo endereco_data
            if not hasattr(estudio, 'endereco_data'):
                raise AttributeError("O objeto estudio não possui o atributo endereco_data")

            # Primeiro cria o endereço
            sql_endereco = """
                INSERT INTO endereco 
                (rua, numero, bairro, cidade, complemento, uf, cep, data_cadastro, data_atualizacao) 
                VALUES (%(rua)s, %(numero)s, %(bairro)s, %(cidade)s, %(complemento)s, 
                        %(uf)s, %(cep)s, %(data_cadastro)s, %(data_atualizacao)s)
            """
            endereco_data = {
                'rua': estudio.endereco_data.get('rua', 'Não informado'),
                'numero': estudio.endereco_data.get('numero', 0),
                'bairro': estudio.endereco_data.get('bairro', 'Não informado'),
                'cidade': estudio.endereco_data.get('cidade', ''),
                'complemento': estudio.endereco_data.get('complemento', 'Não informado'),
                'uf': estudio.endereco_data.get('uf', ''),
                'cep': estudio.endereco_data.get('cep', ''),
                'data_cadastro': estudio.endereco_data.get('data_cadastro', datetime.now()),
                'data_atualizacao': estudio.endereco_data.get('data_atualizacao', datetime.now())
            }
            
            self.cursor.execute(sql_endereco, endereco_data)
            id_endereco = self.cursor.lastrowid
            
            # Depois cria o estúdio
            sql_estudio = """
                INSERT INTO estudio 
                (id_perfil, id_endereco, nome, cnpj, descricao, login, senha, tipo, foto_perfil) 
                VALUES (%(id_perfil)s, %(id_endereco)s, %(nome)s, %(cnpj)s, %(descricao)s, 
                        %(login)s, %(senha)s, %(tipo)s, %(foto_perfil)s)
            """
            estudio_data = {
                'id_perfil': estudio.id_perfil,
                'id_endereco': id_endereco,
                'nome': estudio.nome,
                'cnpj': estudio.cnpj,
                'descricao': estudio.descricao,
                'login': estudio.login,
                'senha': estudio.senha,
                'tipo': estudio.tipo,
                'foto_perfil': estudio.foto_perfil
            }
            
            self.cursor.execute(sql_estudio, estudio_data)
            self.conexao.commit()
            return self.cursor.lastrowid
            
        except Error as err:
            self.conexao.rollback()
            raise Exception(f"Erro ao criar estúdio: {err.msg}")
        except Exception as e:
            self.conexao.rollback()
            raise Exception(f"Erro inesperado ao criar estúdio: {str(e)}")

    def buscar_por_id(self, id_estudio):
        """Busca um estúdio pelo ID"""
        try:
            sql = """
                SELECT e.*, en.rua, en.numero, en.bairro, en.cidade, en.complemento, en.uf, en.cep
                FROM estudio e
                JOIN endereco en ON e.id_endereco = en.id_endereco
                WHERE e.id_estudio = %s
            """
            self.cursor.execute(sql, (id_estudio,))
            return self.cursor.fetchone()
        except Error as err:
            raise Exception(f"Erro ao buscar estúdio: {err.msg}")

    def listar_todos(self):
        """Lista todos os estúdios cadastrados"""
        try:
            sql = """
                SELECT e.*, en.rua, en.numero, en.bairro, en.cidade, en.uf
                FROM estudio e
                JOIN endereco en ON e.id_endereco = en.id_endereco
                ORDER BY e.nome
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except Error as err:
            raise Exception(f"Erro ao listar estúdios: {err.msg}")

    def atualizar(self, estudio):
        """Atualiza os dados de um estúdio"""
        try:
            # Verifica se o objeto estudio tem o atributo endereco_data
            if not hasattr(estudio, 'endereco_data'):
                raise AttributeError("O objeto estudio não possui o atributo endereco_data")

            # Primeiro atualiza o endereço
            sql_endereco = """
                UPDATE endereco SET
                rua = %(rua)s,
                numero = %(numero)s,
                bairro = %(bairro)s,
                cidade = %(cidade)s,
                complemento = %(complemento)s,
                uf = %(uf)s,
                cep = %(cep)s,
                data_atualizacao = %(data_atualizacao)s
                WHERE id_endereco = %(id_endereco)s
            """
            endereco_data = {
                'rua': estudio.endereco_data.get('rua'),
                'numero': estudio.endereco_data.get('numero'),
                'bairro': estudio.endereco_data.get('bairro'),
                'cidade': estudio.endereco_data.get('cidade'),
                'complemento': estudio.endereco_data.get('complemento'),
                'uf': estudio.endereco_data.get('uf'),
                'cep': estudio.endereco_data.get('cep'),
                'data_atualizacao': datetime.now(),
                'id_endereco': estudio.endereco_data.get('id_endereco')
            }
            
            self.cursor.execute(sql_endereco, endereco_data)
            
            # Depois atualiza o estúdio
            sql_estudio = """
                UPDATE estudio SET
                nome = %(nome)s,
                cnpj = %(cnpj)s,
                descricao = %(descricao)s,
                login = %(login)s,
                senha = %(senha)s,
                tipo = %(tipo)s,
                foto_perfil = %(foto_perfil)s
                WHERE id_estudio = %(id_estudio)s
            """
            estudio_data = {
                'nome': estudio.nome,
                'cnpj': estudio.cnpj,
                'descricao': estudio.descricao,
                'login': estudio.login,
                'senha': estudio.senha,
                'tipo': estudio.tipo,
                'foto_perfil': estudio.foto_perfil,
                'id_estudio': estudio.id_estudio
            }
            
            self.cursor.execute(sql_estudio, estudio_data)
            self.conexao.commit()
            return True
            
        except Error as err:
            self.conexao.rollback()
            raise Exception(f"Erro ao atualizar estúdio: {err.msg}")
        except Exception as e:
            self.conexao.rollback()
            raise Exception(f"Erro inesperado ao atualizar estúdio: {str(e)}")

    def deletar(self, id_estudio):
        """Remove um estúdio do banco de dados"""
        try:
            # Primeiro obtém o id_endereco para deletar depois
            sql_get_endereco = "SELECT id_endereco FROM estudio WHERE id_estudio = %s"
            self.cursor.execute(sql_get_endereco, (id_estudio,))
            resultado = self.cursor.fetchone()
            
            if not resultado:
                raise Exception("Estúdio não encontrado")
                
            id_endereco = resultado['id_endereco']
            
            # Deleta o estúdio
            sql_estudio = "DELETE FROM estudio WHERE id_estudio = %s"
            self.cursor.execute(sql_estudio, (id_estudio,))
            
            # Deleta o endereço
            sql_endereco = "DELETE FROM endereco WHERE id_endereco = %s"
            self.cursor.execute(sql_endereco, (id_endereco,))
            
            self.conexao.commit()
            return True
            
        except Error as err:
            self.conexao.rollback()
            raise Exception(f"Erro ao deletar estúdio: {err.msg}")
        except Exception as e:
            self.conexao.rollback()
            raise Exception(f"Erro inesperado ao deletar estúdio: {str(e)}")

    def buscar_por_login(self, login):
        """Busca um estúdio pelo login"""
        try:
            sql = """
                SELECT e.*, en.rua, en.numero, en.bairro, en.cidade, en.complemento, en.uf, en.cep
                FROM estudio e
                JOIN endereco en ON e.id_endereco = en.id_endereco
                WHERE e.login = %s
            """
            self.cursor.execute(sql, (login,))
            return self.cursor.fetchone()
        except Error as err:
            raise Exception(f"Erro ao buscar estúdio por login: {err.msg}")

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados"""
        try:
            if self.conexao.is_connected():
                self.cursor.close()
                self.conexao.close()
        except Error as err:
            raise Exception(f"Erro ao fechar conexão: {err.msg}")