import flet as ft
from ui.ui_dropbox import horas, dias
from ui.ui_botones import create_boton_guardar_modal, create_boton_salir_modal
from ui.ui_text import create_sub_titulo_modal, create_titulo_modal, create_texFiel_fijas
from ui.ui_colors import color_bg
import json
import re


def abril_venta_alcohol_modal(vista) -> ft.AlertDialog:
    with open(r"reportes_saft\src\assets\horario.json", "r", encoding="utf-8") as f:
        datos = json.load(f)

    btn_salir = create_boton_salir_modal()
    btn_guardar = create_boton_guardar_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal("Horario Venta de Bebidas Alcoholicas")
    txt_sub_titulo = create_sub_titulo_modal("Horario Permitido:")
    txt_sub_titulo_dom_jue = create_sub_titulo_modal("DOMINGO A JUEVES:")
    apertura_1 = horas("Horario Apertura")
    apertura_1.value = datos.get("horario1Ape")
    apertura_2 = horas("Horario Apertura")
    apertura_2.value = datos.get("horario2Ape")
    apertura_3 = horas("Horario Apertura")
    apertura_3.value = datos.get("horario3Ape")
    cierre_1 = horas("Horario Cierre")
    cierre_1.value = datos.get("horario1Cie")
    cierre_2 = horas("Horario Cierre")
    cierre_2.value = datos.get("horario2Cie")
    cierre_3 = horas("Horario Cierre")
    cierre_3.value = datos.get("horario3Cie")
    txt_sub_titulo_vier_sab = create_sub_titulo_modal("VIERNES A SABADO:")
    txt_sub_titulo_festivo = create_sub_titulo_modal("DIAS FESTIVOS:")
    txt_sub_titulo = create_sub_titulo_modal("Horario Permitido:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,

        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                ft.Divider(),
                txt_sub_titulo_dom_jue,
                ft.Row(controls=[
                    apertura_1,
                    cierre_1,
                ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Divider(),
                txt_sub_titulo_vier_sab,
                ft.Row(controls=[
                    apertura_2,
                    cierre_2,
                ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Divider(),
                txt_sub_titulo_festivo,
                ft.Row(controls=[
                    apertura_3,
                    cierre_3,
                ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Divider(),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            col=12,
            alignment=ft.MainAxisAlignment.CENTER,         # centra verticalmente
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centra horizontalmente
            expand=True
        ),
        actions=[
            btn_salir,
            btn_guardar
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
