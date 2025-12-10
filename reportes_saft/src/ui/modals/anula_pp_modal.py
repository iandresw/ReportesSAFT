import flet as ft
from ui.ui_botones import create_boton_salir_modal, create_boton_aceptar
from ui.ui_text import create_sub_titulo_modal, create_texFiel_fijas, create_titulo_modal
from ui.ui_colors import color_bg


def abrir_anula_plan_pago(vista, e):
    vista.identidad = ft.Ref[ft.TextField]()
    txt_identidad = create_texFiel_fijas(
        "Numero de Identidad", read_only=False, ref=vista.identidad)
    btn_aceptar = create_boton_aceptar()
    btn_aceptar.on_click = vista.anular_plan_pago
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal("Anular Planes de Pago")
    txt_sub_titulo = create_sub_titulo_modal(
        "Ingrese el numero de identidad o R.T.M.:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                ft.Divider(),
                txt_identidad,
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
            btn_aceptar,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
