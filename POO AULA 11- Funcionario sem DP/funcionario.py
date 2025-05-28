class Funcionario:
    def __init__(self, nome: str, salario: float):
        self.__nome = nome
        self.__salario = salario

    @property
    def nome(self):
        return self.__nome
        
    @property
    def salario(self):
        return self.__salario 