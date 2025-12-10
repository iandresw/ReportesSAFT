# ui/reportes/eventos_reportes.py

import os
import asyncio
from reports.mora_bi_aldea_anio_report import MoravsBIAldeaAnioReport
from reports.excel.analisis_ingresos_rpt import AnalisisIngresosReport
from reports.mora_bi_report import MoraBIReport
from reports.mora_ics_report import MoraICSReport
from reports.mora_sp_report import MoraSPReport
from reports.mora_vs_ingresos_aldea_report import MoravsIngresosAldeaReport
from reports.trancicion_report import TrancicionReport
from ui.reports.utils_reportes import (
    ejecutar_reporte, snack_inicio_reporte, snack_final_reporte, snack_error_reporte
)


def obtener_titulo_impuesto(impuesto):
    return {
        "1": "BIENES INMUEBLES",
        "2,3": "INDUSTRIA COMERCIO Y SERVICIOS",
        "4": "IMPUESTO PERSONAL",
        "5": "SERVICIOS PUBLICOS",
        "7": "PLANES DE PAGO",
        "0,1,2,3,4,5,7": "TODAS LAS FACTURAS",
        "0": "OTRAS TASAS E IMPUESTOS"
    }.get(impuesto, "DESCONOCIDO, NO-CLASIFICADO")


async def generar_mora_bi(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "mora_bi_report.pdf",
        obtener_datos=lambda: (
            vista.mora_bi.obtener_mora_bi_sami()
            if vista.datos_system["TpoCuenta"]
            else vista.mora_bi.obtener_mora_bi_gob()
        ),
        construir_reporte=lambda datos: MoraBIReport(
            datos, vista.datos_muni, "BIENES INMUEBLES"
        ),
        tipo="pdf"
    )


async def generar_mora_ip(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "mora_ip_report.pdf",
        obtener_datos=lambda: vista.mora_ip.obtener_mora_ip(),
        construir_reporte=lambda datos: MoraBIReport(
            datos, vista.datos_muni, "IMPUESTO PERSONAL"
        ),
        tipo="pdf"
    )


async def generar_mora_ics(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "mora_ics_report.pdf",
        obtener_datos=lambda: (
            vista.mora_ics.obtener_mora_ics_sami()
            if vista.datos_system['TpoCuenta']
            else vista.mora_ics.obtener_mora_ics_gob()
        ),
        construir_reporte=lambda datos: MoraICSReport(
            *datos, municipio=vista.datos_muni, titulo_reporte="INDUSTRIA, COMERCIO Y SERVICIO"
        ),
        tipo="pdf"
    )


async def generar_mora_sp(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "mora_sp_report.pdf",
        obtener_datos=lambda: vista.mora_sp.obtener_mora_sp_sami(),
        construir_reporte=lambda datos: MoraSPReport(
            *datos, municipio=vista.datos_muni, titulo_reporte="SERVICIOS Y TASAS MUNICIPALES"
        ),
        tipo="pdf"
    )


async def generar_excel_mora_vs_ingresos(vista, e):
    impuesto = vista.tipo_impuesto.current.value
    titulo_rpt = obtener_titulo_impuesto(impuesto)

    if not impuesto:
        snack_error_reporte(vista.page, "Tipo de factura no selecionado")
        return

    vista.cerrar_modal()

    await ejecutar_reporte(
        vista,
        e,
        "mora_vs_ingresos_gral.xlsx",
        obtener_datos=lambda: vista.mora_aldea.mora_vs_ingresos_general(
            impuesto),
        construir_reporte=lambda datos: MoravsIngresosAldeaReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )


async def generar_pdf_mora_vs_ingresos(vista, e):
    impuesto = vista.tipo_impuesto.current.value
    titulo_rpt = obtener_titulo_impuesto(impuesto)

    if not impuesto:
        snack_error_reporte(vista.page, "Tipo de factura no selecionado")
        return

    vista.cerrar_modal()

    await ejecutar_reporte(
        vista,
        e,
        "mora_vs_ingresos_gral.pdf",
        obtener_datos=lambda: vista.mora_aldea.mora_vs_ingresos_general(
            impuesto),
        construir_reporte=lambda datos: MoravsIngresosAldeaReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="pdf"
    )


async def generar_reporte_trancicicon(vista, e):
    await ejecutar_reporte(
        vista,
        e,
        "trancicion_report.pdf",
        obtener_datos=lambda: vista.trancicion.obtener_contribuyentes(),
        construir_reporte=lambda datos: TrancicionReport(
            *datos, municipio=vista.datos_muni, titulo_reporte="IMPUESTO PERSONAL"
        ),
        tipo="pdf"
    )


async def generar_reporte_trancicicon_det_ip(vista, e):
    nombre_archivo = "trancicion_report_detalle_ip.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_ip(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_bi(vista, e):
    nombre_archivo = "trancicion_report_detalle_bi.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_bi(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_ics(vista, e):
    nombre_archivo = "trancicion_report_detalle_ics.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_ics(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_ist(vista, e):
    nombre_archivo = "trancicion_report_detalle_ist.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_ist(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_amb(vista, e):
    nombre_archivo = "trancicion_report_detalle_amb.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_amb(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_reporte_trancicicon_det_sp(vista, e):
    nombre_archivo = "trancicion_report_detalle_sp.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)
        vista.trancicion_detalle.obtener_contribuyentes_sp(ruta)
        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)
        os.startfile(ruta)
    except Exception as ex:
        snack_error_reporte(vista.page, ex)


async def generar_mora_bi_aldea_anio_pdf(vista, e):
    ubicacion = vista.ubicacion.current.value
    cod_aldea = vista.cod_aldea.current.value
    titulo_rpt = "Reporte Mora vs Ingresos BI - Año"

    if not cod_aldea:
        snack_error_reporte(vista.page, "No ha Seleccionada una Aldea")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "moral_vs_aldea_bi_anio.pdf",
        obtener_datos=lambda: vista.mora_aldea.mora_bi_ubicacion(
            cod_aldea, ubicacion),
        construir_reporte=lambda datos: MoravsBIAldeaAnioReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="pdf"
    )


async def generar_mora_bi_aldea_anio_excel(vista, e):
    ubicacion = vista.ubicacion.current.value
    cod_aldea = vista.cod_aldea.current.value
    titulo_rpt = "Reporte Mora vs Ingresos BI - Año"

    if not cod_aldea:
        snack_error_reporte(vista.page, "No ha Seleccionada una Aldea")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "moral_vs_aldea_bi_anio.xlsx",
        obtener_datos=lambda: vista.mora_aldea.mora_bi_ubicacion(
            cod_aldea, ubicacion),
        construir_reporte=lambda datos: MoravsBIAldeaAnioReport(
            datos, vista.datos_muni, titulo_rpt
        ),
        tipo="excel"
    )


async def generar_analisis_ingresos(vista, e):
    anio = vista.anio.current.value
    titulo_rpt = f"Analis de Ingresos  vs"

    if not anio:
        snack_error_reporte(vista.page, "debe de ingresar un año")
        return
    vista.cerrar_modal()
    await ejecutar_reporte(
        vista,
        e,
        "analisis_ingresos.xlsx",
        obtener_datos=lambda: vista.analisis.analisis_ingresos_anio_act_anio_ant(
            anio),
        construir_reporte=lambda datos: AnalisisIngresosReport(
            datos, vista.datos_muni, titulo_rpt, anio
        ),
        tipo="excel"
    )


async def anula_plan_pago(vista, e):
    identidad = vista.identidad.current.value
    titulo_rpt = f"Analis de Ingresos  vs"

    if not identidad:
        snack_error_reporte(
            vista.page, "debe de ingresar una identidad valida")
        return
    vista.cerrar_modal()
    await vista.plan_pago.planes_de_pago(identidad=identidad)
