from imposto import Imposto

class INSS(Imposto):
    def calcular(self, valor: float):
        return valor * 0.1