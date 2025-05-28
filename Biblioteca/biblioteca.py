class Biblioteca:
    def __init__(self, nome, cnpj, aluno, endereco, obras  ):
        self._nome = nome
        self._cnpj = cnpj
        self.aluno = aluno #agregação
        self._endereco = endereco
        self._obras = obras