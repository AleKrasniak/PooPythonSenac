from conta import Conta
from pessoa import Pessoa
from  cliente import Cliente
# from historico import Historico

c1 = Cliente('Rodrigo','Viecheneski', '045.477.268-77')
c2 = Cliente('Pedro', 'Godinho', '777.777.777-77')
m1 = Conta('123-4', c1, 120.0, 1000.0)
m2 = Conta('456-7', c2, 100.0, 500.0)


m1.depositar(100.00)
m1.extrato()
m1.sacar(50.00)
m1.extrato()
m1.transferencia(m2, 100.00)
m1.extrato()
m1.historico.imprime()