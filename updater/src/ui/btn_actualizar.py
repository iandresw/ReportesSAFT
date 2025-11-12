import flet as ft


def create_update_button() -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text="Actualizar aplicación",
        icon=ft.Icons.SYSTEM_UPDATE,
        color=ft.Colors.BLUE_700,
        width=200,
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, ft.Colors.BLUE_700),
            bgcolor='#1b263b',
            shadow_color='#E06C75',
            text_style=ft.TextStyle(
                    size=10,
                    italic=False,
                    font_family="Tahoma",
            ),
            alignment=ft.Alignment(0, 0),
        ),
    )
