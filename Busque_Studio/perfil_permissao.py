from perfil import Perfil
from permissao import Permissao

class Perfil_Permissao:
    def __init__(self, id_perfil_permissao = None, id_perfil = None, id_permissao = None):
        self.id_perfil_permissao = id_perfil_permissao
        self.id_perfil = id_perfil
        self.id_permissao = id_permissao











# CREATE TABLE PERFIL_PERMISSAO(
# ID_PERFIL INT NOT NULL,
# ID_PERMISSAO INT NOT NULL,
# PRIMARY KEY (ID_PERFIL, ID_PERMISSAO),
# FOREIGN KEY (ID_PERFIL) REFERENCES PERFIL(ID_PERFIL)
# ON UPDATE CASCADE
# ON DELETE CASCADE,
# FOREIGN KEY (ID_PERMISSAO) REFERENCES PERMISSAO(ID_PERMISSAO)
# ON UPDATE CASCADE
# ON DELETE CASCADE
