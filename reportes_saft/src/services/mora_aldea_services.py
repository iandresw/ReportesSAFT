from repositories.mora_aldeas_repository import MoraAldeasRepository
from services.parametro_service import ParametroService
import pandas as pd


class MoraAldeaService:
    def __init__(self, conexion, sistem):
        self.repo_mora = MoraAldeasRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def mora_vs_ingresos_general(self, tipo_impuesto):
        mora_vs_ingreso = self.repo_mora.mora_vs_ingresos_general(
            tipo_impuesto)

        if not mora_vs_ingreso:
            raise ValueError(
                "No se encontraron datos de mora general de aldeas (respuesta vacía).")
        try:
            df = pd.DataFrame(mora_vs_ingreso)
        except Exception as e:
            raise ValueError(f"No se pudo convertir a DataFrame: {e}")
        if df.empty:
            raise ValueError(
                "No se encontraron datos de mora general de aldeas  (DataFrame vacío).")
        return df

    def mora_bi_ubicacion(self, cod_aldea, ubicacion):
        data_res = self.repo_mora.mora_bi_ubicacion(
            cod_aldea=cod_aldea, ubicacion=ubicacion)

        if not data_res:
            raise ValueError(
                "No se encontraron datos de mora de bienes inmuebles por aldea y año (respuesta vacía).")
        try:
            df = pd.DataFrame(data_res)
        except Exception as e:
            raise ValueError(f"No se pudo convertir a DataFrame: {e}")
        if df.empty:
            raise ValueError(
                "No se encontraron datos de mora de bienes inmuebles por aldea y año  (DataFrame vacío).")
        return df
