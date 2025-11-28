from repositories.analisis_ingresos_repository import AnalisisIngresosRepository
from services.parametro_service import ParametroService
import pandas as pd


class AnalisisIngresosService:
    def __init__(self, conexion, sistem):
        self.reposicion = AnalisisIngresosRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def analisis_ingresos_anio_act_anio_ant(self, anio: int):
        data = self.reposicion.analisis_ingresos_anio_act_anio_ant(anio)
        if not data:
            raise ValueError(
                "No se encontraron datos de mora general de aldeas (respuesta vacía).")
        try:
            df = pd.DataFrame(data)
        except Exception as e:
            raise ValueError(f"No se pudo convertir a DataFrame: {e}")
        if df.empty:
            raise ValueError(
                "No se encontraron datos de mora general de aldeas  (DataFrame vacío).")
        return df
