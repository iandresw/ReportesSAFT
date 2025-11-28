import flet as ft


def build_layout(titulo_mora, contenedor_mora, titulo_otros, contenedor_otros):

    frame_mora_rpt = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            expand=True,
            controls=[
                titulo_mora,
                contenedor_mora
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    frame_otros_rpt = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            expand=True,
            controls=[
                titulo_otros,
                contenedor_otros
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    return ft.Container(
        expand=True,
        content=ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                frame_otros_rpt,
                frame_mora_rpt
            ],
        )
    )
