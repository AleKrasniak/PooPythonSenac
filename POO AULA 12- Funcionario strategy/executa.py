from funcionario import Funcionario 
from impostoSalario import ImpostoSalario
from inss import INSS
from irrf import IRRF

funcionario = Funcionario ('Gilson', 4000.00)
imposto_salario = ImpostoSalario()

INSS = imposto_salario.calcular(funcionario.salario, INSS())

IRRF = imposto_salario.calcular(funcionario.salario, IRRF())
print(INSS)
print(IRRF)