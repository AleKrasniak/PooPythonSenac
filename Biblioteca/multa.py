from abc import ABC, abstractmethod
class Multa(ABC): 
    @abstractmethod
    def calcularMulta(self, valor: float):
        pass