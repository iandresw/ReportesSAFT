import flet as ft

from ui.dashboard.components import grafico_mora_por_anio, metric_cards
from ui.dashboard.layout import build_layout
from ui.ui_container import container_titulo, create_container
from services.dashboard_services import DashboardService


class VistaDashBoard:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()

        self._init_services()
        self.titulo_tabla = container_titulo("Dashboard de Mora")
        self.titulo_grafico = container_titulo("Porcentaje de Mora por Año")
        self.row_cards = ft.Row(metric_cards(self))
        self.contenedor_card = create_container(content=self.row_cards)

        self.chart = grafico_mora_por_anio(self)
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Facturas")),
                ft.DataColumn(ft.Text("Mora")),
                ft.DataColumn(ft.Text("% Mora")),
                ft.DataColumn(ft.Text("Monto")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("2020")),
                        ft.DataCell(ft.Text("210")),
                        ft.DataCell(ft.Text("58")),
                        ft.DataCell(ft.Text("27.6%")),
                        ft.DataCell(ft.Text("L. 32,500")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("2021")),
                        ft.DataCell(ft.Text("198")),
                        ft.DataCell(ft.Text("49")),
                        ft.DataCell(ft.Text("24.7%")),
                        ft.DataCell(ft.Text("L. 28,300")),
                    ]
                ),
            ],
        )
        self.layout = build_layout(self.titulo_tabla, self.chart,
                                   self.titulo_grafico, self.data_table, self.contenedor_card)

    def build(self):
        return self.layout

    def _init_services(self):
        self.services = DashboardService(self.app.conexion_saft)
        self.data_card = self.services.obtener_cards()
        self.data_grafico = self.services.obtener_grafico()
