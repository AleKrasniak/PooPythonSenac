class Pessoa:
    def __init__(self, nome, idade, salario):
        self.nome = nome
        self.idade = idade
        self.salario = salario

    def exibeNome(self):
      print("**********\nO nome da pessoa é: {}".format(self.nome))

    def exibeIdade(self):
      print("A idade da pessoa é: {}".format(self.idade))    

    def exibeSalario(self):
      print("A idade da pessoa é: {}\n**********".format(self.salario))  