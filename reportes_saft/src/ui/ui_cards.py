import flet as ft
from ui.ui_colors import color_bg, color_texto


def metric_card(title, value, color="#1976D2"):
    return ft.Container(
        padding=20,
        bgcolor=color_bg(),
        border_radius=10,
        expand=True,
        content=ft.Column(
            [
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                ft.Text(value, size=24,
                        weight=ft.FontWeight.BOLD, color=color),
            ],
            spacing=5,
        ),
    )
