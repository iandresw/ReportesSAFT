from repositories.aldea_repository import AldeaRepository


class AldeaService:
    def __init__(self, conexion):
        self.repository = AldeaRepository(conexion)

    def obtener_aldeas(self):
        data_res = self.repository.obtener_aldeas()
        if not data_res:
            raise ValueError(
                "No se encontraron Aldeas (respuesta vacía).")
        return data_res
