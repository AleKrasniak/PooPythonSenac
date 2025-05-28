from historico import Historico

class Conta:
    def __init__(self, saldo):
        # self._numero = numero
        # self._titular = cliente #o _ serve para encapsular ,eis atributos
        self._saldo = saldo
        # self._limite = limite
        # self.historico = Historico()

    def get_saldo(self):
        return self._saldo
    
    def set_saldo(self,saldo):
        self._saldo = saldo

    # def depositar(self, valor):
    #     self.saldo += valor
    #     self.historico.transacoes.append("Deposito de {}".format(valor))

    # def sacar(self, valor):
    #     if(self.saldo < valor):
    #         return False
    #     else: 
    #         self.saldo -= valor
    #         self.historico.transacoes.append("Saque de {}".format(valor))
    #         return True

    # def extrato(self):
    #     print("Número: {} \nSaldo: {}".format(self.numero, self.saldo))
    #     self.historico.transacoes.append("Tirou extrato - saldo de {}".format(self.saldo))

    # def transferencia(self, destino, valor):
    #     retirou = self.sacar(valor)
    #     if(retirou == False):
    #         return False
    #     else:
    #         destino.depositar(valor)
    #         self.historico.transacoes.append("Transferência de R$ {} para conta {}".format(valor, destino.numero))
    #         return True

