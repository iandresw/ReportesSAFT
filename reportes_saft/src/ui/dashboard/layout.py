import flet as ft
from ui.ui_colors import color_bg


def build_layout(titulo, contenedor_chart, titulo_otros, tabla_aldea, cards):

    chart_container = ft.Container(
        bgcolor="white",
        border_radius=10,
        padding=20,
        content=ft.Column(
            [
                ft.Text(
                    "Porcentaje de Mora por Año",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=300, content=contenedor_chart),
            ]
        ),
    )

    # ----- TABLA -----

    table_container = ft.Container(
        bgcolor="white",
        padding=20,
        border_radius=10,
        content=ft.Column(
            [
                ft.Text(
                    "Detalle de Mora por Año",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                tabla_aldea,
            ]
        ),
    )

    # ----- LEYENDA / NOTA IMPORTANTE -----

    leyenda = ft.Container(
        bgcolor="#FFF3CD",
        padding=15,
        border_radius=8,
        border=ft.border.all(1, "#FFEEBA"),
        content=ft.Row(
            [
                ft.Icon(ft.Icons.INFO, color="#856404"),
                ft.Text(
                    "Los valores mostrados se generan según la facturación registrada en SAFT. "
                    "Si la facturación no está al día, los datos pueden no reflejar los valores correctos, "
                    "sobre todo en Bienes Inmuebles que pueden generar facturación masiva.",
                    color="#856404",
                    size=14,
                ),
            ],
            expand=True,
        ),
    )

    # ----- DISEÑO FINAL -----

    return ft.Column(
        [
            ft.Text("Dashboard de Mora", size=28,
                    weight=ft.FontWeight.BOLD),
            cards,
            ft.Divider(),
            chart_container,
            ft.Divider(),
            table_container,
            ft.Divider(),
            leyenda,
        ],
        spacing=20,
    )
