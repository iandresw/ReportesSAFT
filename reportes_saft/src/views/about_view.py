import webbrowser
import flet as ft
from ui.ui_btn_actualizar import create_update_button
from ui.ui_alertas import AlertaGeneral
from ui.ui_botones import create_boton
from ui.ui_container import container_titulo, create_container
from version import APP_VERSION
from services.parametro_service import ParametroService

from services.update_services import UpdateService


class VistaAbout:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()
        self.ft = ft
        self.parametro_service = ParametroService(self.app.conexion_saft)
        self.datos_muni = self.parametro_service.obtener_datos_municipalidad()
        self.datos_system = self.parametro_service.obtener_datos_systema()

        self.update_app = UpdateService(self.page)

        # BOTONES
        self.btn_update = create_update_button(
            self.page, on_click=self.update_app.verificar_actualizacion)

        self.conten_acerca_de = create_container(
            expand=True,
            height=580,
            col=12,
            controls=[
                ft.Column(
                    alignment=self.ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=self.ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    controls=[
                        ft.Image(src=r"\assets\saft.png"),
                        ft.Text(
                            "Reportes SAFT",
                            size=24,
                            weight=self.ft.FontWeight.BOLD,
                            text_align=self.ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            f"Versión {APP_VERSION}",
                            size=16,
                            color=self.ft.Colors.BLUE_400,
                        ),
                        ft.Text(
                            "Herramienta desarrollada por la Unidad SAFT - AMHON.\n"
                            "Permite la generación de reportes, consultas datos municipales.\n\n",
                            size=14,
                            color=self.ft.Colors.GREY_700,
                            text_align=self.ft.TextAlign.CENTER,
                        ),
                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.TextButton(
                                    "🌐 Página AMHON",
                                    on_click=lambda e: webbrowser.open(
                                        "https://www.amhon.hn"
                                    ),
                                ), ft.TextButton(
                                    "🌐 Portal SAFT",
                                    on_click=lambda e: webbrowser.open(
                                        "http://saftamhon.com"
                                    ),
                                )
                            ],
                        ),
                        ft.Divider(),
                        self.btn_update,
                        ft.Text(
                            "© 2025 Asociación de Municipios de Honduras (AMHON)",
                            size=12,
                            color=self.ft.Colors.GREY_600,
                            italic=True,
                            text_align=self.ft.TextAlign.CENTER,
                        ),
                        ft.Row([
                            ft.Container(
                                ft.Image(src='/saft.png', width=50, height=40)),
                            ft.Container(
                                ft.Image(src='/Logo_amhon.png', width=100, height=90))
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ],
                )
            ],
        )
        self.frame = ft.Container(
            expand=True,
            content=ft.ResponsiveRow(
                controls=[

                    self.conten_acerca_de,
                ],
                alignment=ft.MainAxisAlignment.CENTER, col=12
            )
        )

    def build(self):
        return ft.Column([
            self.frame
        ])
