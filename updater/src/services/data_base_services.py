from repositories.data_base_repository import DataBaseRepository


class DataBaseService:
    def __init__(self, conexion):
        self.repository = DataBaseRepository(conexion)

    def alterar_parametro_cont(self):
        return self.repository.parametroCont()
