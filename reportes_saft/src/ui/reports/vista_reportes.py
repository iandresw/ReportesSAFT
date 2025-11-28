# ui/reportes/vista_reportes.py

import asyncio
import datetime
from ui.reports.layout_reportes import build_layout
from ui.reports.botones_reportes import botones_mora, botones_otros
from ui.ui_container import container_titulo, create_container
from ui.reports.eventos_reportes import (generar_analisis_ingresos, generar_mora_bi, generar_mora_bi_aldea_anio_excel, generar_mora_bi_aldea_anio_pdf, generar_mora_ics, generar_mora_ip,
                                         generar_mora_sp, generar_pdf_mora_vs_ingresos, generar_excel_mora_vs_ingresos, generar_reporte_trancicicon,
                                         generar_reporte_trancicicon_det_amb, generar_reporte_trancicicon_det_bi,
                                         generar_reporte_trancicicon_det_ics, generar_reporte_trancicicon_det_ip,
                                         generar_reporte_trancicicon_det_ist, generar_reporte_trancicicon_det_sp)
from ui.modals.mora_aldea_bi_modal import abrir_modal_mora_bi_aldea_anio
from ui.modals.mora_vs_ingresos_aldea_modal import abrir_modal_mora_vs_ingresos
from ui.modals.analisi_ingresos_modal import abrir_analisis_ingresos
from services.aldea_servives import AldeaService
from services.parametro_service import ParametroService
from services.mora_bi_services import MoraBIService
from services.mora_ip_services import MoraIPService
from services.mora_ics_sevices import MoraICSService
from services.mora_sp_services import MoraSPService
from services.update_services import UpdateService
from services.mora_aldea_services import MoraAldeaService
from services.trancicion_traspaso_servivces import TrancicionTraspasoService
from services.trancicion_traspaso_det_services import TrancicionTraspasoDetalleService
from services.analisis_ingresos_services import AnalisisIngresosService


class VistaReportes:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()

        # servicios y datos
        self._init_services()

        # titulos
        self.titulo_mora = container_titulo("REPORTES DE MORA")
        self.titulo_otros = container_titulo("OTROS REPORTES")

        # botones
        self.contenedor_mora = create_container(botones_mora(self))
        self.contenedor_otros = create_container(botones_otros(self))

        # layout
        self.layout = build_layout(
            self.titulo_mora,
            self.contenedor_mora,
            self.titulo_otros,
            self.contenedor_otros
        )

    def build(self):
        return self.layout

    def _init_services(self):
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
        self.aldeas = AldeaService(self.app.conexion_saft)
        self.mora_aldea = MoraAldeaService(
            self.app.conexion_saft, self.datos_system)
        self.analisis = AnalisisIngresosService(
            self.app.conexion_saft, self.datos_system)

    # BOTONES DE TRANCISION
    def rept_trancicicon(self, e):
        asyncio.run(generar_reporte_trancicicon(self, e))

    def rpt_trancicion_det_ip(self, e):
        asyncio.run(generar_reporte_trancicicon_det_ip(self, e))

    def rpt_trancicion_det_bi(self, e):
        asyncio.run(generar_reporte_trancicicon_det_bi(self, e))

    def rpt_trancicion_det_ics(self, e):
        asyncio.run(generar_reporte_trancicicon_det_ics(self, e))

    def rpt_trancicion_det_amp(self, e):
        asyncio.run(generar_reporte_trancicicon_det_amb(self, e))

    def rpt_trancicion_det_ist(self, e):
        asyncio.run(generar_reporte_trancicicon_det_ist(self, e))

    def rpt_trancicion_det_sp(self, e):
        asyncio.run(generar_reporte_trancicicon_det_sp(self, e))

    # BOTONES MORA

    def on_mora_bi(self, e):
        asyncio.run(generar_mora_bi(self, e))

    def on_mora_ip(self, e):
        asyncio.run(generar_mora_ip(self, e))

    def on_mora_ics(self, e):
        asyncio.run(generar_mora_ics(self, e))

    def on_mora_sp(self, e):
        asyncio.run(generar_mora_sp(self, e))
    # ABRIR MODALS

    def abrir_modal_mora_vs_ingresos(self, e):
        self.tipo_impuesto = 0
        self.dialog = abrir_modal_mora_vs_ingresos(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abrir_modal_mora_aldea_anio(self, e):
        self.ubicacion = 0
        self.cod_aldea = ''
        self.dialog = abrir_modal_mora_bi_aldea_anio(self, e)
        self.page.open(self.dialog)
        self.page.update()

    def abril_modal_analisi_ingresos(self, e):
        self.anio = (datetime.date.year)
        self.dialog = abrir_analisis_ingresos(self, e)
        self.page.open(self.dialog)
        self.page.update()
    # CERRAR MODALS

    def cerrar_modal(self):
        self.dialog.open = False
        self.page.update()

    def generar_excel_aldea_mora(self, e):
        asyncio.run(generar_excel_mora_vs_ingresos(self, e))

    def generar_pdf_aldea_mora(self, e):
        asyncio.run(generar_pdf_mora_vs_ingresos(self, e))

    def generar_excel_mora_bi_aldea_anio(self, e):
        asyncio.run(generar_mora_bi_aldea_anio_excel(self, e))

    def generar_pdf_mora_bi_aldea_anio(self, e):
        asyncio.run(generar_mora_bi_aldea_anio_pdf(self, e))

    def generar_exel_analisi_ingresos(self, e):
        asyncio.run(generar_analisis_ingresos(self, e))
