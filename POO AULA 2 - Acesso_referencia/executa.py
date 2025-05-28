from conta import Conta
from pessoa import Pessoa

c1 = Conta('123-4','Rodrigo', 120.0, 1000.0)
c2 = Conta('234-5', 'Nandinho', 300.00, 1200.0)
# c1 é um atributo de referência para um objeto para que isso ocorra no python são acionados de forma transparente os métodos mágicos  
# __new__() e __init__() respons´veis por construir e iniciar objetos. 
#c3 = Conta('999-9','Bruno', 50000.0, 200.0) 
c3 = Conta('123-4','Rodrigo', 120.0, 1000.0)

# print(c2.saldo)
# c2.depositar(0.50)
# print(c2.saldo)

# print(c1.saldo)
# c1.depositar(10000.0)
# print(c1.saldo)

if(c1 == c3):
    print("Contas são iguais")
else:
    print("Contas são diferentes")


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