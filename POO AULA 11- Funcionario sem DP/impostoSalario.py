class ImpostoSalario:
    def calcular(self, salario: float, imposto: str):
        if imposto == 'INSS':
            return salario * 0.1
        if imposto == 'IRRF':
            return salario  * 0.25
        return 0.0