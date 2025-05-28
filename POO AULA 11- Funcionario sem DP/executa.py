from funcionario import Funcionario 
from impostoSalario import ImpostoSalario

funcionario = Funcionario ('Pedro Dias',10000.00)
imposto_salario = ImpostoSalario()

INSS = imposto_salario.calcular(funcionario.salario, 'INSS')

print(INSS)