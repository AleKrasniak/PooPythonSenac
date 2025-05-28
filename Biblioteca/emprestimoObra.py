# from historicoemprestimo import Historicoemprestimo
# class EmprestimoObra:
#     def __init__(self, aluno, numero_obra, nome,status="disponível"):
#         self._aluno = aluno
#         self._numero_obra = numero_obra
#         self._nome = nome
#         self._status = status
#         self.historicoemprestimo = Historicoemprestimo()


    
#     def emprestar(self):
#         if self.status == "disponível":
#             self.status = "emprestado"
#             print(f"Obra emprestada com sucesso. para o aluno {self.aluno.nome}")
#             self.historicoemprestimo.emprestimo.append("Obra Emprestada : {}".format(self.numero_obra))
#         else:
#             print(f"Obra {self.numero_obra} não está disponível para empréstimo.")

#     def devolver(self):
#         if self.status == "emprestado":
#             self.status = "disponível"
#             print(f"Obra devolvida pelo aluno {self.aluno.nome}.")
#             self.historicoemprestimo.devolucao.append("Obra devolvida : {}".format(self.numero_obra))
#         else:
#             print(f"Obra {self.numero_obra} já está disponível.")

from historicoemprestimo import Historicoemprestimo
from obra import Obra
from aluno import Aluno

class EmprestimoObra:
    def __init__(self, aluno, obra, status='disponível'):
        self._aluno = aluno #agregação
        self._obra = obra
        self._status = status
        self.historicoemprestimo = Historicoemprestimo() #historico

    def emprestar(self):
        if self._status == "disponível":
            self._status = "emprestado"
            print(f"Obra emprestada com sucesso. para o aluno {Aluno.get_str(self)}.")
            self.historicoemprestimo._emprestimo.append(f"Obra Emprestada : {Obra.get_str(self)}")
        else:
            print(f"Obra {Obra.get_str(self)} não está disponível para empréstimo.")
    
    def devolver(self):
        if self._status == "emprestado":
            self._status = "disponível"
            print(f"Obra devolvida pelo aluno {Aluno.get_str(self)}.")
            self.historicoemprestimo._devolucao.append(f"Obra devolvida : {Obra.get_str(self)}")
        else:
            print(f"Obra {Obra.get_str(self)} já está disponível.")

#ALUNO
    def get_aluno(self, ):
        return self._aluno
    
    def set_aluno(self):
        return self._aluno
    
#NUMERO OBRA
    
    def get_numero_obra(self):
        return self._obra
    
    def set_numero_obra(self,):
        return self._obra
    
    def get_status(self):
        return self._status
    
    def set_status(self,):
        return self._status
    

