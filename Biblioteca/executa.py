import datetime
from biblioteca import Biblioteca
from aluno import Aluno
from emprestimoObra import EmprestimoObra
from historicoemprestimo import Historicoemprestimo
from funcionario import Funcionario 
from bibliotecario import Bibliotecario
from obra import Obra
from multa import Multa
from multaAtraso import multaAtraso
from valorMultaEmprestimo import ValorMultaEmpresrtimo


aluno1 =Aluno('Alessandra','Krasniak', '888.888', 'ADS')
b1 = Biblioteca('SenacBooks', '000.000.0008/5', aluno1, 'João Manuel dos Santos Ribas', 'Abordagem banco de dados')
obra1 = Obra('Avatar','ficção')
em = EmprestimoObra(aluno=aluno1, obra=obra1, status='disponivel')
hist = Historicoemprestimo ()

hist._datadevolucao = hist._dataPrevistaDevolucao + datetime.timedelta(days=8)

Func = Funcionario ("Fernando","35","000.111.222-3","1234567", "666", 2500)

Biblio= Bibliotecario ("Gilson",28,"111.000.000-5", "Bibliotecario", "123654", 3000, "789",  8)

multa= multaAtraso(historico=hist, emprestimo=em, valor_dia=5.0)
multa.imprimirMulta()


# em.emprestar()
# hist.imprimiremprestimo()
# em.emprestar()
# print("\n")
# em.devolver()
# hist.imprimirdevolucao()
# print("\n")

# print(Biblio.get_bonificacao())
# print("\n")
# print(Func.get_bonificacao())
# print("\n")

# Func.get_descontosalario()
# Biblio.get_descontosalario()



