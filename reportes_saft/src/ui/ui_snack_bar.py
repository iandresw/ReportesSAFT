from flet import SnackBar, Row, ProgressRing, Text, FontWeight
from ui.ui_colors import color_bg_snack, color_bg_snack_error, color_texto, color_check


def snack_inicio(mensaje: str):
    content = Row([ProgressRing(height=20,
                                width=20,
                                color=color_texto()), Text(f'{mensaje}', size=14, color=color_texto(), weight=FontWeight.W_200)])
    return SnackBar(content=content,
                    bgcolor=color_bg_snack(),
                    duration=3000
                    )


def snack_rpt_generado(nombre_archivo: str):
    content = Text(f"Reporte generado: {nombre_archivo}, Arbiendo archivo...",
                   size=14, color=color_texto(), weight=FontWeight.W_200)
    return SnackBar(content=content,
                    bgcolor=color_bg_snack(),
                    duration=3000
                    )


def snack_error(error: str):
    content = Text(f"Error: {error}", size=14)
    return SnackBar(content=content,
                    bgcolor=color_bg_snack_error(),
                    duration=3000
                    )
