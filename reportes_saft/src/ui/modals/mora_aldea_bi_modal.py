import flet as ft
from ui.ui_radio import rd_ubicacion
from ui.ui_dropbox import dropbox_aldeas
from ui.ui_botones import crear_boton_excel, create_boton_pdf, create_boton_salir_modal
from ui.ui_text import create_sub_titulo_modal, create_titulo_modal
from ui.ui_colors import color_bg


def abrir_modal_mora_bi_aldea_anio(vista, e):
    vista.ubicacion = ft.Ref[ft.RadioGroup]()
    vista.cod_aldea = ft.Ref[ft.Dropdown]()
    radio_ubicacion = rd_ubicacion(vista.ubicacion)
    data_aldeas = vista.aldeas.obtener_aldeas()
    dropbox_ald = dropbox_aldeas(data_aldeas, vista.cod_aldea)
    btn_excel = crear_boton_excel()
    btn_excel.on_click = vista.generar_excel_mora_bi_aldea_anio
    btn_pdf = create_boton_pdf()
    btn_pdf.on_click = vista.generar_pdf_mora_bi_aldea_anio
    btn_salir = create_boton_salir_modal()
    btn_salir.on_click = lambda _: vista.cerrar_modal()
    txt_titulo = create_titulo_modal(
        "Generar Mora de Bienes Inmuebles Año/aldea")
    txt_sub_titulo = create_sub_titulo_modal("Seleccione la Ubicacion:")
    return ft.AlertDialog(
        modal=True,
        bgcolor=color_bg(),
        title=txt_titulo,
        content=ft.Column(
            controls=[
                ft.Divider(),
                txt_sub_titulo,
                radio_ubicacion,
                ft.Divider(),
                dropbox_ald,
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
