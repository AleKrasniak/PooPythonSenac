class Obra:
    def __init__(self, titulo, tipo, status='dispinível'):
        self.__titulo = titulo
        self.__tipo = tipo


    def get_str(self):
         return self.__titulo
    def set_str(self):
         return self.__titulo