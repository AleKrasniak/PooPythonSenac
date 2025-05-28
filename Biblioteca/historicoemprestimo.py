import datetime

#encapsulamento
class Historicoemprestimo:
    def __init__(self):
        self._dataemprestimo = datetime.datetime.now()
        self._datadevolucao = datetime.datetime.now()
        self._dataPrevistaDevolucao = self._dataemprestimo + datetime.timedelta(days=7)
        self._devolucao = []
        self._emprestimo = [] 
    
    def imprimiremprestimo(self):
        print("Data Emprestimo {}".format(self._dataemprestimo.strftime("%d/%m/%Y %H:%M")))
        print("Data prevista de devolução {}".format(self._dataPrevistaDevolucao.strftime("%d/%m/%Y %H:%M")))

    
    def imprimirdevolucao(self):
        print("Data Devolução {}".format(self._datadevolucao.strftime("%d/%m/%Y %H:%M")))



@property
def dataemprestimo(self):
    return self._dataemprestimo

@dataemprestimo.setter
def dataemprestimo(self, value):
    self._dataemprestimo = value

@property
def datadevolucao(self):
    return self._datadevolucao

@datadevolucao.setter
def datadevolucao(self, value):
    self._datadevolucao = value

@property
def dataPrevistaDevolucao(self):
    return self._dataPrevistaDevolucao

@dataPrevistaDevolucao.setter
def dataPrevistaDevolucao(self, value):
    self._dataPrevistaDevolucao = value