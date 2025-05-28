from imposto import Imposto

class IRRF(Imposto):
    def calcular(self, valor: float):
        return valor * 0.25