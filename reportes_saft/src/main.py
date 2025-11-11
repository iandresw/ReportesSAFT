import flet as ft
from contexts.app_context import AppContext
from views.permiso_operacion_view import VistaPermisoOperacion
from ui.ui_container import create_container_rail
from views.about_view import VistaAbout
from views.reportes_view import VistaReportes
from ui.ui_colors import color_bg, color_bg_2, color_shadow, color_texto

from services.parametro_service import ParametroService


def main(page: ft.Page):
    context = AppContext()
    text_color = color_texto()
    context.init_saft()
    parametro_service = ParametroService(context.conexion_saft)
    datos_muni = parametro_service.obtener_datos_municipalidad()
    datos_system = parametro_service.obtener_datos_systema()
    # --- Configuración ventana ---
    page.window.maximizable = False
    page.window.resizable = False
    x_height = 680
    x_width = 600
    page.window.width = x_width
    page.window.height = x_height
    page.window.max_height = x_height
    page.window.min_height = x_height
    page.window.max_width = x_width
    page.window.min_width = x_width

    # --- Título superior ---
    titulo_muni = ft.Text(
        f"{datos_muni['NombreMuni']} - {datos_muni['NombreDepto']}",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color=text_color
    )

    # --- Crear las vistas ---
    view_reportes = VistaReportes(page, context).build()
    view_about = VistaAbout(page, context).build()
    view_permiso_operacion = VistaPermisoOperacion(page, context).build()

    # --- Contenedor dinámico donde se cargan las vistas ---
    main_content = ft.Container(
        expand=True,
        content=view_reportes  # vista inicial
    )

    # --- Función para cambiar vista según selección ---
    def on_nav_change(e):
        index = e.control.selected_index
        if index == 0:
            main_content.content = view_reportes
        elif index == 2:
            main_content.content = view_permiso_operacion
        elif index == 1:
            main_content.content = view_about
        page.update()

    # --- Menú lateral (NavigationRail) ---
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        indicator_color=color_bg(),
        indicator_shape=ft.RoundedRectangleBorder(radius=5),
        selected_label_text_style=ft.TextStyle(),
        bgcolor=color_bg_2(),
        leading=ft.Image(src="/saft.png", width=50),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.VIEW_COMFORTABLE_OUTLINED,

                selected_icon=ft.Icons.VIEW_COMFORTABLE_ROUNDED,
                label_content=ft.Text("Reportes",  color=text_color),
                indicator_color=color_shadow(),
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ARCHIVE_OUTLINED,
                selected_icon=ft.Icons.ARCHIVE_ROUNDED,
                label_content=ft.Text("P.O.", color=text_color),
                indicator_color=color_shadow(),
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ARCHIVE_OUTLINED,
                selected_icon=ft.Icons.ARCHIVE_ROUNDED,
                label_content=ft.Text("Acerca De", color=text_color),
                indicator_color=color_shadow(),
            ),
        ],
        on_change=on_nav_change,  # ← aquí cambiamos la vista
    )

    con_rail = create_container_rail(
        content=rail,
        expand=False
    )
    # --- Fondo principal ---
    page.bgcolor = color_bg()

    # --- Layout general ---
    page.add(
        ft.Column(
            [
                ft.Row([titulo_muni]),
                ft.Row(
                    [
                        con_rail,
                        ft.VerticalDivider(width=2),
                        main_content,  # donde se muestran las vistas
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
    )


ft.app(main)
