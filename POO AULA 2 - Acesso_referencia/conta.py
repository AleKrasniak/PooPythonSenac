class Conta:
    def __init__(self, numero, titular, saldo, limite=1000.0):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo
        self.limite = limite

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        self.saldo -= valor
        if(self.saldo < valor):
            return False
        else: 
            return True

    def extrato(self):
        print("Número: {} \nSaldo: {}".format(self.numero, self.saldo))


