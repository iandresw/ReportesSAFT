from repositories.prescripcion_repository import PrescripcionesRepository


class PrescripcionService:
    def __init__(self, conexion):
        self.repository = PrescripcionesRepository(conexion)

    def obtener_analisi(self):
        data_res = self.repository.obtenter_analis_prescripcion
        if not data_res:
            raise ValueError(
                "No se encontraron datos para analisi de prescripcion (respuesta vacía).")
        return data_res
