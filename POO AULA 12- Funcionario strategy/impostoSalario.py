from imposto import Imposto

class ImpostoSalario:
    def calcular(self, salario:float, imposto: Imposto):
        return imposto.calcular(salario)