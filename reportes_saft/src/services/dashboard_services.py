from repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, conexion):
        self.repositorio = DashboardRepository(conexion)

    def obtener_cards(self):
        datos = []
        datos_res = self.repositorio.obtener_valores_cards()
        print(datos_res)
        datos.append({
            'TotalGenerado': datos_res['TotalGenerado'],
            'TotalFacturas': datos_res['TotalFacturas'],
            'MoraTotalFacturas': datos_res['MoraTotalFacturas'],
            'MoraTotal': datos_res['MoraTotal'],
            'IngresosTotalFacturas': datos_res['IngresosTotalFacturas'],
            'Ingresos': datos_res['Ingresos'],
            'PorcentajeMora': datos_res['PorcentajeMora'],
            'PorcentajeIngresos': datos_res['PorcentajeIngresos'],
        })
        return datos

    def obtener_grafico(self):
        return self.repositorio.obtener_valores_grafico()
