import flet as ft
from ui.ui_radio import rd_tipo_factura
from ui.ui_botones import crear_boton_excel, create_boton_pdf, create_boton_salir_modal
from ui.ui_text import create_sub_titulo_modal, create_titulo_modal
from ui.ui_colors import color_bg


def abrir_modal_mora_vs_ingresos(vista, e) -> ft.AlertDialog:
    vista.tipo_impuesto = ft.Ref[ft.RadioGroup]()
    radio_group = rd_tipo_factura(vista.tipo_impuesto)
    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_excel_aldea_mora
    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_pdf_aldea_mora
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal("Generar Mora vs Ingresos")
    txt_sub_titulo = create_sub_titulo_modal(
        "Seleccione tipo de impuesto:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                radio_group,
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
            btn_pdf,
            btn_excel,
            btn_salir
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
