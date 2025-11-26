import flet as ft
import os
import logging
import webbrowser
import asyncio
from ui.ui_alertas import AlertaGeneral
from ui.ui_botones import create_boton
from ui.ui_container import color_bg, color_bg_2, container_titulo, create_container
from ui.ui_radio import rd_tipo_factura
from ui.ui_snack_bar import snack_inicio, snack_rpt_generado, snack_error
from ui.ui_colors import color_texto, color_texto_2, color_texto_parrafo, color_shadow, color_borde

from services.parametro_service import ParametroService
from services.mora_bi_services import MoraBIService
from services.mora_ip_services import MoraIPService
from services.mora_ics_sevices import MoraICSService
from services.mora_sp_services import MoraSPService
from services.update_services import UpdateService
from services.mora_aldea_services import MoraAldeaService
from services.trancicion_traspaso_servivces import TrancicionTraspasoService
from services.trancicion_traspaso_det_services import TrancicionTraspasoDetalleService
from reports.trancicion_report import TrancicionReport
from reports.mora_sp_report import MoraSPReport
from reports.mora_ics_report import MoraICSReport
from reports.mora_bi_report import MoraBIReport
from reports.mora_vs_ingresos_aldea_report import MoravsIngresosAldeaReport
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/logs_rpt_py.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class VistaReportes:
    def __init__(self, page: ft.Page, context):
        self.page = page
        self.app = context
        self.app.init_saft()
        self.ft = ft
        self.parametro_service = ParametroService(self.app.conexion_saft)
        self.datos_muni = self.parametro_service.obtener_datos_municipalidad()
        self.datos_system = self.parametro_service.obtener_datos_systema()
        self.mora_bi = MoraBIService(self.app.conexion_saft, self.datos_system)
        self.mora_ip = MoraIPService(self.app.conexion_saft, self.datos_system)
        self.mora_ics = MoraICSService(
            self.app.conexion_saft, self.datos_system)
        self.mora_sp = MoraSPService(self.app.conexion_saft, self.datos_system)
        self.update_app = UpdateService(self.page)
        self.trancicion = TrancicionTraspasoService(
            self.app.conexion_saft, self.datos_system)
        self.trancicion_detalle = TrancicionTraspasoDetalleService(
            self.app.conexion_saft, self.datos_system)

        self.mora_aldea = MoraAldeaService(
            self.app.conexion_saft, self.datos_system)

        self.conten_titulo_mora_rpt = container_titulo("REPORTES DE MORA")
        self.conten_titulo_otras_rpt = container_titulo("OTROS REPORTES")
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

        self.btn_mora_vs_ingresos_general = create_boton(
            text_label="Mora vs Ingresos por Adea General", on_click=self.abrir_modal_mora_vs_ingresos)

        self.btn_trancicon_traspaso = create_boton(
            text_label="Trancición y Traspaso", on_click=self.generar_reporte_trancicicon)

        self.btn_trancicon_ip_detalle = create_boton(
            text_label="Trancición y Traspaso Detalle IP", on_click=self.generar_reporte_trancicicon_det_ip)
        self.btn_trancicon_bi_detalle = create_boton(
            text_label="Trancición y Traspaso Detalle BI", on_click=self.generar_reporte_trancicicon_det_bi)

        self.btn_trancicon_ics_detalle = create_boton(
            text_label="Trancición y Traspaso Detalle ICS", on_click=self.generar_reporte_trancicicon_det_ics)

        self.btn_trancicon_amb_detalle = create_boton(
            text_label="Trancición y Traspaso Detalle AMB", on_click=self.generar_reporte_trancicicon_det_amb)

        self.btn_trancicon_ist_detalle = create_boton(
            text_label="Trancición y Traspaso Detalle IST", on_click=self.generar_reporte_trancicicon_det_ist)
        self.btn_trancicon_sp_detalle = create_boton(
            text_label="Trancición y Traspaso Detalle SP", on_click=self.generar_reporte_trancicicon_det_sp)

        self.conten_btn_mora_rpt = create_container(
            controls=[
                self.btn_mora_bi,
                self.btn_mora_ip,
                self.btn_mora_ics,
                self.btn_mora_sp,
                self.btn_mora_vs_ingresos_general
            ],
            expand=True,
            col=12
        )

        self.content_btn_otras_rpt = create_container(
            controls=[
                self.btn_trancicon_traspaso,
                self.btn_trancicon_ip_detalle,
                self.btn_trancicon_bi_detalle,
                self.btn_trancicon_ics_detalle,
                self.btn_trancicon_amb_detalle,
                self.btn_trancicon_ist_detalle,
                self.btn_trancicon_sp_detalle
            ],
            expand=True,
            col=12
        )

        self.frame_mora_rpt = ft.Container(
            expand=True,
            alignment=ft.Alignment(1, 1),
            content=ft.ResponsiveRow(
                controls=[
                    self.conten_titulo_mora_rpt,
                    self.conten_btn_mora_rpt,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.frame_otros_rpt = ft.Container(
            expand=True,
            alignment=ft.Alignment(1, 1),
            content=ft.ResponsiveRow(
                controls=[
                    self.conten_titulo_otras_rpt,
                    self.content_btn_otras_rpt,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.frame_1_2 = ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Row([
                        self.frame_otros_rpt,
                        self.frame_mora_rpt,
                    ],)
                ]
            )

        )

    def build(self):
        return self.frame_1_2

    def cargar_snack_final(self, nombre_archivo, e):
        e.control.disabled = False
        # e.control.style.bgcolor = color_bg_2()
        e.control.update()
        snack_fin = snack_rpt_generado(nombre_archivo)
        self.page.open(snack_fin)
        self.page.update()

    def cargar_snack_errr(self, error):
        snack_err = snack_error(str(error))
        logging.error(f"Error Generar Reporte: {error}", exc_info=True)
        self.page.open(snack_err)
        self.page.update()

    def cargar_snack_inicio(self, mensaje, e):
        e.control.disabled = True
        # e.control.style.bgcolor = color_bg()
        e.control.update()
        snack_ini = snack_inicio(str(mensaje))
        self.page.open(snack_ini)
        self.page.update()

    async def generar_reporte_mora_bi(self, e):
        nombre_archivo = "mora_ip_report.pdf"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            if self.datos_system['TpoCuenta']:
                datos = self.mora_bi.obtener_mora_bi_sami()
            else:
                datos = self.mora_bi.obtener_mora_bi_gob()
            reporte = MoraBIReport(datos, self.datos_muni, "BIENES INMUEBLES")
            reporte.generar_pdf(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            webbrowser.open_new_tab(f"file://{ruta}")
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_mora_ip(self, e):
        nombre_archivo = "mora_ip_report.pdf"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            datos = self.mora_ip.obtener_mora_ip()
            reporte = MoraBIReport(datos, self.datos_muni, "IMPUESTO PERSONAL")
            reporte.generar_pdf(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            webbrowser.open_new_tab(f"file://{ruta}")
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_mora_ics(self, e):
        nombre_archivo = "mora_ics_report.pdf"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            if self.datos_system['TpoCuenta']:
                datos_i, datos_c, datos_s, datos_t = self.mora_ics.obtener_mora_ics_sami()
            else:
                datos_i, datos_c, datos_s, datos_t = self.mora_ics.obtener_mora_ics_gob()
            reporte = MoraICSReport(
                datos_i, datos_c, datos_s, datos_t, self.datos_muni, "INDUSTRIA, COMERCIO Y SERVICIO")
            reporte.generar_pdf(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            webbrowser.open_new_tab(f"file://{ruta}")
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_mora_vs_ingresos_general(self, e):
        nombre_archivo = "mora_vs_ingresos_gral.pdf"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            datos = self.mora_aldea.mora_vs_ingresos_general()

            await asyncio.sleep(0.5)
            reporte = MoravsIngresosAldeaReport(
                datos, self.datos_muni, "vs INGRESOS POR ALDEA")
            reporte.generar_pdf(ruta)
            ruta_excel = reporte.generar_execel()
            os.startfile(ruta_excel)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            webbrowser.open_new_tab(f"file://{ruta}")
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_mora_sp(self, e):
        nombre_archivo = "mora_sp_report.pdf"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            (datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques,
             datos_lim_cementerio, datos_ase_cementerio, datos_ambiente, datos_contribucion) = self.mora_sp.obtener_mora_sp_sami()
            reporte = MoraSPReport(datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques,
                                   datos_lim_cementerio, datos_ase_cementerio, datos_ambiente, datos_contribucion, self.datos_muni, "SERVICIOS Y TASAS MUNICIPALIES")
            reporte.generar_pdf(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            webbrowser.open_new_tab(f"file://{ruta}")
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_trancicicon(self, e):
        nombre_archivo = "trancicion_report.pdf"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            datos, datos_cat, datos_sp = self.trancicion.obtener_contribuyentes()
            reporte = TrancicionReport(
                datos, datos_cat, datos_sp, self.datos_muni, "TRANCICION Y TRASPASO")
            reporte.generar_pdf(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            webbrowser.open_new_tab(f"file://{ruta}")
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_trancicicon_det_ip(self, e):
        nombre_archivo = "trancicion_report_detalle_ip.xlsx"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            self.trancicion_detalle.obtener_contribuyentes_ip(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            os.startfile(ruta)
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_trancicicon_det_bi(self, e):
        nombre_archivo = "trancicion_report_detalle_bi.xlsx"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            self.trancicion_detalle.obtener_contribuyentes_bi(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            os.startfile(ruta)
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_trancicicon_det_ics(self, e):
        nombre_archivo = "trancicion_report_detalle_ics.xlsx"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            self.trancicion_detalle.obtener_contribuyentes_ics(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            os.startfile(ruta)
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_trancicicon_det_amb(self, e):
        nombre_archivo = "trancicion_report_detalle_amb.xlsx"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            self.trancicion_detalle.obtener_contribuyentes_amb(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            os.startfile(ruta)
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_trancicicon_det_ist(self, e):
        nombre_archivo = "trancicion_report_detalle_ist.xlsx"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            self.trancicion_detalle.obtener_contribuyentes_ist(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            os.startfile(ruta)
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_reporte_trancicicon_det_sp(self, e):
        nombre_archivo = "trancicion_report_detalle_sp.xlsx"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            await asyncio.sleep(0.5)
            self.trancicion_detalle.obtener_contribuyentes_sp(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            os.startfile(ruta)
        except Exception as ex:
            self.cargar_snack_errr(ex)

    def abrir_modal_mora_vs_ingresos(self, e):
        self.tipo_impuesto = ft.Ref[ft.RadioGroup]()
        radio_group = rd_tipo_factura(self.tipo_impuesto)

        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor=color_bg(),
            title=ft.Text("Generar Mora vs Ingresos",
                          color=color_texto(), size=15, font_family="Tahoma", text_align=ft.TextAlign.CENTER),
            content=ft.Column(
                controls=[
                    ft.Text("Seleccione tipo de impuesto:",
                            color=color_texto(), size=10, font_family="Tahoma", text_align=ft.TextAlign.CENTER),
                    radio_group,
                ],
                tight=True,
                scroll=ft.ScrollMode.AUTO,
                col=12,
                alignment=ft.MainAxisAlignment.CENTER,         # centra verticalmente
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centra horizontalmente
                expand=True
            ),

            actions=[
                ft.ElevatedButton("PDF", icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
                                  on_click=self.generar_pdf_mora_vs_ingresos, color=color_borde(),

                                  style=ft.ButtonStyle(
                                      side=ft.BorderSide(2, color_borde()),
                                      shape=ft.RoundedRectangleBorder(
                                          radius=18),
                                      bgcolor=color_bg_2(),
                                      shadow_color=color_shadow(),
                                      text_style=ft.TextStyle(
                                          size=11, font_family="Tahoma", color=color_borde()),
                                  )),
                ft.ElevatedButton("Excel", icon=ft.Icons.BACKUP_TABLE_ROUNDED,
                                  on_click=self.generar_excel_mora_vs_ingresos, color=color_borde(),

                                  style=ft.ButtonStyle(
                                      side=ft.BorderSide(2, color_borde()),
                                      shape=ft.RoundedRectangleBorder(
                                          radius=18),
                                      bgcolor=color_bg_2(),
                                      shadow_color=color_shadow(),
                                      text_style=ft.TextStyle(
                                          size=11, font_family="Tahoma", color=color_borde()),
                                  )),
                ft.ElevatedButton("Salir", icon=ft.Icons.EXIT_TO_APP, color=color_borde(),

                                  style=ft.ButtonStyle(
                                      side=ft.BorderSide(2, color_borde()),
                                      shape=ft.RoundedRectangleBorder(
                                          radius=18),
                                      bgcolor=color_bg_2(),
                                      shadow_color=color_shadow(),
                                      text_style=ft.TextStyle(
                                          size=11, font_family="Tahoma", color=color_borde()),
                ),
                    on_click=lambda _: self.cerrar_modal())
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.page.open(self.dialog)
        self.page.update()

    def cerrar_modal(self):
        self.dialog.open = False
        self.page.update()

    async def generar_pdf_mora_vs_ingresos(self, e):
        impuesto = self.tipo_impuesto.current.value
        if impuesto == "1":
            titulo_rpt = "BIENES INMUEBLES"
        elif impuesto == "2,3":
            titulo_rpt = "INDUSTRIA COMERCIO Y SERVICIOS"
        elif impuesto == "4":
            titulo_rpt = "IMPUESTO PERSONAL"
        elif impuesto == "5":
            titulo_rpt = "SERVICIOS PUBLICOS"
        elif impuesto == "7":
            titulo_rpt = "PLANES DE PAGO"
        elif impuesto == "0,1,2,3,4,5,7":
            titulo_rpt = "TODAS LAS FACTURAS"
        elif impuesto == "0":
            titulo_rpt = "OTRAS TASAS E IMPUESTOS"
        else:
            titulo_rpt = "DESCONOCIDO, NO-CLASIFICADO"
        if not impuesto:
            self.page.open(snack_error("Seleccione un tipo de impuesto"))
            return
        self.cerrar_modal()
        nombre_archivo = "mora_vs_ingresos_gral.pdf"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            datos = self.mora_aldea.mora_vs_ingresos_general(impuesto)

            await asyncio.sleep(0.5)
            reporte = MoravsIngresosAldeaReport(
                datos, self.datos_muni, titulo_rpt)
            reporte.generar_pdf(ruta)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
            webbrowser.open_new_tab(f"file://{ruta}")
        except Exception as ex:
            self.cargar_snack_errr(ex)

    async def generar_excel_mora_vs_ingresos(self, e):
        impuesto = self.tipo_impuesto.current.value
        if impuesto == "1":
            titulo_rpt = "BIENES INMUEBLES"
        elif impuesto == "2,3":
            titulo_rpt = "INDUSTRIA COMERCIO Y SERVICIOS"
        elif impuesto == "4":
            titulo_rpt = "IMPUESTO PERSONAL"
        elif impuesto == "5":
            titulo_rpt = "SERVICIOS PUBLICOS"
        elif impuesto == "7":
            titulo_rpt = "PLANES DE PAGO"
        elif impuesto == "0,1,2,3,4,5,7":
            titulo_rpt = "TODAS LAS FACTURAS"
        elif impuesto == "0":
            titulo_rpt = "OTRAS TASAS E IMPUESTOS"
        else:
            titulo_rpt = "DESCONOCIDO, NO-CLASIFICADO"

        if not impuesto:
            self.page.open(snack_error("Seleccione un tipo de factura"))
            return

        self.cerrar_modal()
        nombre_archivo = "mora_vs_ingresos_gral.xlsx"
        ruta = os.path.join(os.getcwd(), nombre_archivo)
        try:
            self.cargar_snack_inicio(f"Iniciando reporte: {nombre_archivo}", e)
            datos = self.mora_aldea.mora_vs_ingresos_general(impuesto)
            await asyncio.sleep(0.5)
            reporte = MoravsIngresosAldeaReport(
                datos, self.datos_muni, titulo_rpt)
            ruta_excel = reporte.generar_execel()
            os.startfile(ruta_excel)
            self.cargar_snack_final(nombre_archivo=nombre_archivo, e=e)
            await asyncio.sleep(0.5)
        except Exception as ex:
            self.cargar_snack_errr(ex)
