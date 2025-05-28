from conta import Conta
from pessoa import Pessoa

#conta = Conta('123-4', 'mensalão', 120.0, 1000.0) --- SEM ACESSO POR REFERÊNCIA
# c1 é um atributo de referência para um objeto para que isso ocorra no python são acionados de forma transparente os métodos mágicos  
# __new__() e __init__() responsáveis por construir e iniciar objetos. 

c1 = Conta('123-4','Rodrigo', 120.0, 1000.0)
c2 = Conta('234-5', 'Gilson', 10.00, 1200.0)
c3 = Conta('123-4','Rodrigo', 120.0, 1000.0)

#deposito e saque

print(c2.saldo)
c1.depositar(100.0)
print(c1.saldo)
c2.depositar(300.0)
print(c2.saldo)
c2.transferencia(c1,30)
print(c1.saldo)
print(c2.saldo)


if(c1 == c2):
    print("Contas são iguais")
else:
    print("Contas são diferentes")



#CASO EM QUE A CONTA SERIA IGUAL------------------

# if(c1.numero == c3.numero):
#     print("Contas são iguais")
# else:
#     print("Contas são diferentes")

#IMPRIMIR METODOS DA CONTA------------
# print(c2.saldo)
# c2.depositar(0.50)
# print(c2.saldo)

# print(c1.saldo)
# c1.depositar(10000.0)
# print(c1.saldo)

#CLASSE PESSOA, ATRIBUINDO OS DADOS
p1 = Pessoa('Alessandra','20', '1580.0')
p2 = Pessoa('Dragon','5', '0')
p3 = Pessoa('Nandinho','35','100000.0')
p4 = Pessoa('Gustavo','22','1800.0')

#CHAMANDO O MÉTODO

p1.exibeNome(), p1.exibeIdade(), p1.exibeSalario()
p2.exibeNome(), p2.exibeIdade(), p2.exibeSalario()
p3.exibeNome(), p3.exibeIdade(), p3.exibeSalario()
p4.exibeNome(), p4.exibeIdade(), p4.exibeSalario()

