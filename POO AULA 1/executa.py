from conta import Conta #instânciar classe conta


conta = Conta('123-4', 'mensalão', 120.0, 1000.0)
type(conta)

conta.extrato()

conta.saldo = 1000
print(conta.saldo)

print(conta.titular)

conta.depositar(2250.0)
conta.extrato()

conta.sacar(200.0)
conta.extrato()

consegui = conta.sacar(222.0)
if(consegui):
    print("Consegui sacar")
    print("Restam ainda: {}".format(conta.saldo))
else:
    print("Saldo insuficiente")