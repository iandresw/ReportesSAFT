import flet as ft
import os
import webbrowser
from ui.ui_alertas import AlertaGeneral
from ui.ui_botones import create_boton
from ui.ui_container import container_titulo, create_container

from services.parametro_service import ParametroService
from services.mora_bi_services import MoraBIService
from services.mora_ip_services import MoraIPService
from services.mora_ics_sevices import MoraICSService
from services.mora_sp_services import MoraSPService
from services.update_services import UpdateService
from services.trancicion_traspaso_servivces import TrancicionTraspasoService
from reports.trancicion_report import TrancicionReport
from reports.mora_sp_report import MoraSPReport
from reports.mora_ics_report import MoraICSReport
from reports.mora_bi_report import MoraBIReport


class VistaReportes:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()
        self.ft = ft
        self.parametro_service = ParametroService(self.app.conexion_saft)
        self.datos_muni = self.parametro_service.obtener_datos_municipalidad()
        self.datos_system = self.parametro_service.obtener_datos_systema()
        self.mora_bi = MoraBIService(self.app.conexion_saft, self.datos_system)
        self.mora_ip = MoraIPService(self.app.conexion_saft, self.datos_system)
        self.update_app = UpdateService(self.page)
        self.mora_ics = MoraICSService(
            self.app.conexion_saft, self.datos_system)
        self.trancicion = TrancicionTraspasoService(
            self.app.conexion_saft, self.datos_system)
        self.mora_sp = MoraSPService(
            self.app.conexion_saft, self.datos_system)

        self.titulo_mensajes = container_titulo("Mensajes")
        self.conten_titulo_mora_rpt = container_titulo(
            "REPORTES DE MORA")
        self.conten_titulo_otras_rpt = container_titulo(
            "OTROS REPORTES")
        self.conten_titulo_reportes = container_titulo("Reportes")
        self.conten_titulo_resultados = container_titulo("Caja Resultado")

        # BOTONES

        self.btn_mora_bi = create_boton(
            text_label="Mora Bienes Innuebles", on_click=self.generar_reporte_mora_bi)

        self.btn_mora_ip = create_boton(
            text_label="Mora Impuesto Personal", on_click=self.generar_reporte_mora_ip)

        self.btn_mora_ics = create_boton(
            text_label="Mora Impuesto Industria, Comercio Y Servicio", on_click=self.generar_reporte_mora_ics)

        self.btn_mora_sp = create_boton(
            text_label="Mora Servicios Publicos", on_click=self.generar_reporte_mora_sp)

        self.btn_trancicon_traspaso = create_boton(
            text_label="Trancición y Traspaso", on_click=self.generar_reporte_trancicicon)

        self.conten_mensajes = create_container(
            expand=True,
            controls=[ft.Column(controls=[],
                                scroll=ft.ScrollMode.AUTO)],
            col=12)

        self.conten_btn_mora_rpt = create_container(
            controls=[ft.Row(
                alignment=self.ft.MainAxisAlignment.CENTER,
                controls=[self.ft.Column(
                    alignment=self.ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.btn_mora_bi,
                        self.btn_mora_ip,
                        self.btn_mora_ics,
                        self.btn_mora_sp,
                    ]
                )
                ]
            )],
            expand=True,
            height=538,
            col=12
        )

        self.content_btn_otras_rpt = create_container(
            controls=[ft.Row(
                alignment=self.ft.MainAxisAlignment.START,
                controls=[self.ft.Column(
                    alignment=self.ft.MainAxisAlignment.START,
                    controls=[
                        self.btn_trancicon_traspaso
                    ]
                )
                ]
            )],
            expand=True,
            height=538,
            col=12
        )

        self.frame_mora_rpt = ft.Container(
            expand=True,
            content=ft.ResponsiveRow(
                controls=[
                    self.conten_titulo_mora_rpt,
                    self.conten_btn_mora_rpt,
                ],
                alignment=ft.MainAxisAlignment.CENTER, col=4
            )
        )
        self.frame_otros_rpt = ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 1),
            content=ft.ResponsiveRow(
                controls=[
                    self.conten_titulo_otras_rpt,
                    self.content_btn_otras_rpt,
                ],
                alignment=ft.MainAxisAlignment.CENTER, col=4
            )
        )
        self.frame_1_2 = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Row([
                        self.frame_otros_rpt,
                        self.frame_mora_rpt,
                    ])
                ]
            )

        )

    def build(self):
        return ft.Column([
            self.frame_1_2
        ])

    def generar_reporte_mora_bi(self, e):
        try:
            if self.datos_system['TpoCuenta']:
                datos = self.mora_bi.obtener_mora_bi_sami()
            else:
                datos = self.mora_bi.obtener_mora_bi_gob()
            reporte = MoraBIReport(datos, self.datos_muni, "BIENES INMUEBLES")
            nombre_archivo = "mora_bi_report.pdf"
            ruta = os.path.join(os.getcwd(), nombre_archivo)

            reporte.generar_pdf(ruta)
            webbrowser.open_new_tab(f"file://{ruta}")
            # Mostrar notificación
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Reporte generado: {nombre_archivo}", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))

            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))

            self.page.update()

    def generar_reporte_mora_ip(self, e):
        try:
            datos = self.mora_ip.obtener_mora_ip()
            reporte = MoraBIReport(datos, self.datos_muni, "IMPUESTO PERSONAL")
            nombre_archivo = "mora_ip_report.pdf"
            ruta = os.path.join(os.getcwd(), nombre_archivo)

            reporte.generar_pdf(ruta)
            webbrowser.open_new_tab(f"file://{ruta}")
            # Mostrar notificación
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Reporte generado: {nombre_archivo}", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))
            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))

            self.page.update()

    def generar_reporte_mora_ics(self, e):
        try:
            if self.datos_system['TpoCuenta']:
                datos_i, datos_c, datos_s, datos_t = self.mora_ics.obtener_mora_ics_sami()
            else:
                datos_i, datos_c, datos_s, datos_t = self.mora_ics.obtener_mora_ics_gob()
            reporte = MoraICSReport(
                datos_i, datos_c, datos_s, datos_t, self.datos_muni, "INDUSTRIA, COMERCIO Y SERVICIO")
            nombre_archivo = "mora_ics_report.pdf"
            ruta = os.path.join(os.getcwd(), nombre_archivo)

            reporte.generar_pdf(ruta)
            webbrowser.open_new_tab(f"file://{ruta}")
            # Mostrar notificación
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Reporte generado: {nombre_archivo}", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))

            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))

            self.page.update()

    def generar_reporte_mora_sp(self, e):
        try:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Iniciando Reporte", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))

            self.page.update()
            (datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques,
             datos_lim_cementerio, datos_ase_cementerio, datos_ambiente, datos_contribucion) = self.mora_sp.obtener_mora_sp_sami()
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Data Optenida", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))
            reporte = MoraSPReport(datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques,
                                   datos_lim_cementerio, datos_ase_cementerio, datos_ambiente, datos_contribucion, self.datos_muni, "SERVICIOS Y TASAS MUNICIPALIES")
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Renerando Reporte ", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))
            nombre_archivo = "mora_sp_report.pdf"
            ruta = os.path.join(os.getcwd(), nombre_archivo)

            reporte.generar_pdf(ruta)
            webbrowser.open_new_tab(f"file://{ruta}")
            # Mostrar notificación
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Reporte generado: {nombre_archivo}", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))

            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))

            self.page.update()

    def generar_reporte_trancicicon(self, e):
        try:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Iniciando Reporte", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))
            datos, datos_cat, datos_sp = self.trancicion.obtener_contribuyentes()
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Data Optenida", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))
            reporte = TrancicionReport(
                datos, datos_cat, datos_sp, self.datos_muni, "TRANCICION Y TRASPASO")
            nombre_archivo = "trancicion_report.pdf"
            ruta = os.path.join(os.getcwd(), nombre_archivo)

            reporte.generar_pdf(ruta)
            webbrowser.open_new_tab(f"file://{ruta}")
            # Mostrar notificación
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Reporte generado: {nombre_archivo}", size=14),
                bgcolor=ft.Colors.GREEN_700,
            ))

            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))

            self.page.update()
