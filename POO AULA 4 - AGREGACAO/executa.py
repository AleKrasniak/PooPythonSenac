from conta import Conta
from pessoa import Pessoa
from  cliente import Cliente 

c1 = Cliente('Rodrigo','Viecheneski', '045.477.268-77')
c2 = Cliente('Pedro', 'Godinho', '777.777.777-77')
m1 = Conta('123-4', c1, 120.0, 1000.0)
m2 = Conta('456-7', c2, 100.0, 500.0)



print(m1.titular.nome)
print(m1.titular.sobrenome)
print(m1.titular.cpf)

print(m1.__dict__)
print(m1.titular.__dict__)
print("\n")
print(m2.titular.nome)
print(m2.titular.sobrenome)
print(m2.titular.cpf)

print(m2.__dict__)
print(m2.titular.__dict__)

#Relacionamento entre classes 