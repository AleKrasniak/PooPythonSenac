class Funcionario:
    def __init__(self, nome, idade, cpf, cargo, ctps, salario):
        self._nome = nome
        self._idade = idade
        self._cpf = cpf
        self._cargo = cargo
        self._ctps = ctps
        self._salario = salario

    def get_bonificacao(self):
        print("Bonificação bibliotecario R$: ")
        return self._salario * 0.10
    
    def get_descontosalario(self):
        DiasFalta = int(input("Informe os dias de falta do funcionário \n"))
        Desconto = ((self._salario / 30) * DiasFalta )
        self._salario = self._salario - Desconto
        print("Salário Valor descontado e salário: ")
        print (f"Desconto R$ {Desconto:.2f} \nSalário R$ {self._salario:2f} \n")