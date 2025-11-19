from flet import SnackBar, Row, ProgressRing, Text, FontWeight
from ui.ui_colors import color_bg_snack, color_bg_snack_error, color_texto, color_check


def snack_inicio(mensaje: str):
    fila_nack_bar = Row([ProgressRing(height=20,
                                      width=20,
                                      color=color_texto()), Text(f'{mensaje}', size=14, color=color_texto(), weight=FontWeight.W_200)])
    return SnackBar(content=fila_nack_bar, bgcolor=color_bg_snack(),)


def snack_rpt_generado(nombre_archivo: str):
    return SnackBar(content=Text(f"Reporte generado: {nombre_archivo}", size=14, color=color_texto(), weight=FontWeight.W_200), bgcolor=color_bg_snack(),)


def snack_error(error: str):
    return SnackBar(Text(f"Error: {error}", size=14), bgcolor=color_bg_snack_error(), )
