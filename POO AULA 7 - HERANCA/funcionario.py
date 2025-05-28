class Funcionario: 
    def __init__(self, nome, cpf, cargo, salario):
        self._nome = nome
        self._cpf = cpf
        self._cargo = cargo
        self._salario = salario

    def get_bonificacao(self):
        return self._salario * 0.10
    