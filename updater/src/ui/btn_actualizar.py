import flet as ft


def create_update_button() -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text="Actualizar aplicación",
        icon=ft.Icons.SYSTEM_UPDATE,
        color=ft.Colors.BLUE_700,
        width=200,
        height=35,
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


def cerrar_app_boton() -> ft.ElevatedButton:
    return ft.ElevatedButton(
        "Cerrar aplicación y continuar",
        icon=ft.Icons.CLOSE,
        color='#E06C75',
        visible=False,
        width=200,
        height=35,
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, '#E06C75'),
            bgcolor='#1b263b',
            shadow_color='#E06C75',
            text_style=ft.TextStyle(
                    size=10,
                    italic=False,
                    font_family="Tahoma",
                    color='#E06C75',
            ),
            alignment=ft.Alignment(0, 0),
        ))


def actualizar_base_boton() -> ft.ElevatedButton:
    return ft.ElevatedButton(
        "Actualizar Base de Datos",
        icon=ft.Icons.CLOSE,
        color='#E06C75',
        visible=True,
        width=200,
        height=35,
        style=ft.ButtonStyle(
            side=ft.BorderSide(2, ft.Colors.BLUE_700),
            bgcolor='#1b263b',
            shadow_color=ft.Colors.BLUE_700,
            text_style=ft.TextStyle(
                    size=10,
                    italic=False,
                    font_family="Tahoma",
                    color=ft.Colors.BLUE_700,
            ),
            alignment=ft.Alignment(0, 0),
        ))
