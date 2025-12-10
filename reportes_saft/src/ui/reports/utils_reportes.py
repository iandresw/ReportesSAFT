

import asyncio
import logging
import os
import webbrowser
from ui.ui_snack_bar import snack_error, snack_inicio, snack_rpt_generado


def snack_inicio_reporte(page, mensaje, e):
    e.control.disabled = True
    page.open(snack_inicio(mensaje))
    page.update()


def snack_final_reporte(page, nombre, e):
    e.control.disabled = False
    page.open(snack_rpt_generado(nombre))
    page.update()


def snack_error_reporte(page, error):
    logging.error(f"Error Generar Reporte: {error}", exc_info=True)
    page.open(snack_error(str(error)))
    page.update()


async def ejecutar_reporte(
    vista,
    e,
    nombre_archivo,
    obtener_datos,
    construir_reporte=None,
    tipo="pdf",
):
    ruta = os.path.join(os.getcwd(), nombre_archivo)

    try:
        snack_inicio_reporte(
            vista.page, f"Iniciando reporte: {nombre_archivo}", e)
        await asyncio.sleep(0.5)

        # 👇 función que retorna los datos
        datos = obtener_datos()

        # 👇 función que retorna la instancia del reporte
        reporte = construir_reporte(datos)

        # 👇 genera el archivo correspondiente
        if tipo == "pdf":
            reporte.generar_pdf(ruta)
        elif tipo == "excel":
            ruta = reporte.generar_execel()

        snack_final_reporte(vista.page, nombre_archivo, e)
        await asyncio.sleep(0.5)

        # 👇 Abrir archivo
        if tipo == "pdf":
            webbrowser.open_new_tab(f"file://{ruta}")
        else:
            os.startfile(ruta)

    except Exception as ex:
        snack_error_reporte(vista.page, ex)
