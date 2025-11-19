from repositories.parametro_repository import ParametroRepository


class ParametroService:
    def __init__(self, conexion):
        self.repo = ParametroRepository(conexion)

    def obtener_datos_municipalidad(self):
        datos = self.repo.obtener_parametros()
        if not datos:
            raise ValueError(
                "No se encontraron parámetros de la municipalidad.")
        return datos

    def obtener_nombre_municipio(self):
        datos = self.repo.obtener_parametros()
        return datos.get("NombreMuni", "Municipalidad desconocida") if datos else "Sin datos"

    def obtener_datos_systema(self):
        datos = self.repo.obtener_systemParam()
        if not datos:
            raise ValueError(
                "No se encontraron parámetros del systema.")
        return datos

    def obtener_datos_municipalidad_admin(self):
        datos = self.repo.obtener_parametros_cont()
        if not datos:
            raise ValueError(
                "No se encontraron parámetros del systema.")
        return datos
