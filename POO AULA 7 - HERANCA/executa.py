from funcionario import Funcionario 
from gerente import gerente

gere = gerente ("Rodrigo","465461446-165","Gerente", 20000.00, "123", 12)

print(gere.get_bonificacao())
#print (vars(gerente))
gere.autentica("123")
gere.autentica("23")

funcionario = Funcionario("Alessandra","46454646-131", "Analista", 5000.00)

print(funcionario.get_bonificacao())

