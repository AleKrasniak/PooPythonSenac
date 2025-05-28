from datetime import datetime
from emprestimoObra import EmprestimoObra
from multa import Multa
from historicoemprestimo import Historicoemprestimo


class multaAtraso(Multa):
    def __init__(self, historico: Historicoemprestimo, valor_dia:float, emprestimo: EmprestimoObra):
        self.__historico = historico
        self.__valor_dia = valor_dia
        self.__emprestimo = emprestimo
    
    def calcularMulta(self):
        data_devolucao = self.__historico._datadevolucao()
        data_prevista = self.__historico._dataPrevistaDevolucao()


        dias_atraso = (self.__historico._datadevolucao() - self.__historico._dataPrevistaDevolucao()).days


        return max(dias_atraso, 0) * self.__valor_dia
    
    def imprimirMulta(self):
        multa = self.calcularMulta()
        print("\n =======Detalhes da Multa======== \n")
        print(f"Nome do Aluno: {self.__emprestimo._aluno._nome}\n")
        print(f"Nome da Obra:  {self.__emprestimo._obra.get_str()}\n")
        print(f"Data emprestimo: {self.__historico.imprimiremprestimo()}\n")
        print(f"Data devolucao: {self.__historico.imprimirdevolucao()}\n")
        print(f"Dias de atraso: {(self.__historico.datadevolucao() - self.__historico._dataPrevistaDevolucao().day)}\n")
        print(f"Valor multa {multa:.2f}\n")
