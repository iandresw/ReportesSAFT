import os
import webbrowser
import flet as ft
from contexts.app_context import AppContext
from reports.trancicion_report import TrancicionReport
from reports.mora_sp_report import MoraSPReport
from ui.ui_btn_actualizar import create_update_button
from reports.mora_ics_report import MoraICSReport
from reports.mora_bi_report import MoraBIReport
from ui.ui_botones import create_boton
from ui.ui_colors import color_bg
from services.parametro_service import ParametroService
from services.mora_bi_services import MoraBIService
from services.mora_ip_services import MoraIPService
from services.mora_ics_sevices import MoraICSService
from services.mora_sp_services import MoraSPService
from services.update_services import UpdateService
from services.trancicion_traspaso_servivces import TrancicionTraspasoService


class Form(ft.Control):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.ft = ft
        self.app = AppContext()
        self.app.init_saft()

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
        self.btn_update = create_update_button(
            self.page, on_click=self.update_app.verificar_actualizacion)
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

        self.conten = ft.Container(
            expand=True,
            content=self.ft.Row(
                alignment=self.ft.MainAxisAlignment.CENTER,
                controls=[ft.Column(
                    alignment=self.ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.ft.Text("Reportes de Mora"),
                        self.btn_mora_bi,
                        self.btn_mora_ip,
                        self.btn_mora_ics,
                        self.btn_mora_sp,
                        self.btn_trancicon_traspaso,
                        self.btn_update
                    ]
                )]
            )
        )

    def build(self):  # type: ignore # Implementa build manualmente
        return self.conten

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
            (datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques,
             datos_lim_cementerio, datos_ase_cementerio, datos_ambiente) = self.mora_sp.obtener_mora_sp_sami()

            reporte = MoraSPReport(datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques,
                                   datos_lim_cementerio, datos_ase_cementerio, datos_ambiente, self.datos_muni, "SERVICIOS Y TASAS MUNICIPALIES")
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
            datos = self.trancicion.obtener_contribuyentes()
            reporte = TrancicionReport(
                datos, self.datos_muni, "TRANCICION Y TRASPASO")
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

    def build(self):
        return self.conten


def main(page: ft.Page):
    x_height = 680
    x_width = 600
    page.bgcolor = color_bg()
    page.title = f"Modulo Reportes"

    page.window.maximizable = False
    page.window.resizable = False
    page.window.width = x_width
    page.window.height = x_height
    page.window.max_height = x_height
    page.window.min_height = x_height
    page.window.max_width = x_width
    page.window.min_width = x_width
    page.window.maximizable = False
    page.add(Form(page).build())


ft.app(target=main)
