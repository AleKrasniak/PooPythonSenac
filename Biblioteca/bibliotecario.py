from funcionario import Funcionario 

class Bibliotecario(Funcionario):
    def __init__(self, nome, idade, cpf, cargo, ctps, salario, senha, qnt_bibliotecarios):
        super().__init__(nome, idade, cpf,cargo, ctps, salario)
        self.salario = salario
        self._senha= senha
        self._qnt_bibliotecarios = qnt_bibliotecarios
    
    def autenticarSenha(self, senha):
        if self._senha == senha:
            print("Acesso Liberado")
            return True
        
        else: 
            print("Acesso Negado")
            return False
    
    def getBonificacao(self):
        print("Bonificação Bibliotecário R$: ")
        return super().get_bonificacao() + 500
    
    def get_descontosalario(self, DiasFalta=None):
        DiasFalta = int(input("Informe os dias de falta do funcionário \n"))
        Desconto = ((self._salario / 30) * DiasFalta )
        self._salario = self._salario - Desconto
        print("Salário Valor descontado e salário: ")
        print (f"Desconto R$ {Desconto:.2f} \nSalário R$ {self._salario:2f} \n")
    

    