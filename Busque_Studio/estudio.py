from datetime import datetime
from perfil import Perfil

class Estudio:
    def __init__(self, id_estudio=None, id_perfil=None, nome=None, cnpj=None, 
                 descricao=None, login=None, senha=None, tipo=None, email=None,
                 telefone=None, foto_perfil=None, rua=None, numero=None, 
                 bairro=None, cidade=None, complemento=None, uf=None, cep=None,
                 data_cadastro=None, data_atualizacao=None):
        self.id_estudio = id_estudio
        self.id_perfil = id_perfil
        self.nome = nome
        self.cnpj = cnpj
        self.descricao = descricao
        self.login = login
        self.senha = senha
        self.tipo = tipo
        self.email = email
        self.telefone = telefone
        self.foto_perfil = foto_perfil
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.complemento = complemento
        self.uf = uf
        self.cep = cep
        self.data_cadastro = data_cadastro or datetime.now()
        self.data_atualizacao = data_atualizacao or datetime.now()

    def validar(self):
        campos_obrigatorios = [
            self.nome, self.cnpj, self.login, self.senha, 
            self.tipo, self.email, self.telefone, self.cidade, 
            self.uf, self.cep
        ]
        
        if not all(campos_obrigatorios):
            return False
            
        if len(self.cnpj) != 14 or not self.cnpj.isdigit():
            return False
            
        if len(self.senha) < 6:
            return False
            
        return True