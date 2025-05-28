from abc import ABC, abstractmethod
class Imposto(ABC):
    @abstractmethod
    def calcular(self, valor: float):
        pass 