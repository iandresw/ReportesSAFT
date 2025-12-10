import flet as ft
import logging
import os
from contexts.app_context import AppContext
from ui.dashboard.vista_dashboard import VistaDashBoard
from views.permiso_operacion_view import VistaPermisoOperacion
from ui.ui_container import create_container_rail
from views.about_view import VistaAbout
# from views.reportes_view import VistaReportes
from ui.ui_colors import color_bg, color_bg_2, color_shadow, color_texto
from services.parametro_service import ParametroService
from ui.reports.vista_reportes import VistaReportes
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/logs_rpt_py.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class UILayout(ft.Container):
    def __init__(self, page: ft.Page, context):
        super().__init__(expand=True)
        self.page = page
        self.x_width = 900
        self.x_height = 710
        # self.page.window.width = 900
        # self.page.window.height = 90
        # self.page.window.center()
        self.page.window.max_height = 1000000
        self.page.window.min_height = 800
        self.page.window.max_width = 10000
        self.page.window.min_width = 1024
        self.page.window.maximizable = True
        self.page.window.minimizable = True
        self.page.window.resizable = True
        self.page.title = "Reportes SAFT"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 15
        self.context = context
        self.context.init_saft()
        self.page.window.icon = "assets/icon.ico"
        self.page.update()
        text_color = color_texto()
        bg_color = color_bg()
        bg_2_color = color_bg_2()
        shadow_color = color_shadow()
        parametro_service = ParametroService(self.context.conexion_saft)
        datos_muni = parametro_service.obtener_datos_municipalidad()
        datos_system = parametro_service.obtener_datos_systema()
        self.user = self.context.usuario_actual

        municipalidad = datos_muni['NombreMuni'].rstrip().replace(
            "Municipalidad de", "")

        # --- Título superior ---
        self.titulo_muni = ft.Text(
            f"Municipalidad de {municipalidad} - {datos_muni['NombreDepto'].replace(" ", "")}",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color=text_color
        )
        user = self.user.username
        self.user_info = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Text("Cerrar sesión",
                                    color=color_texto()),
                    on_click=lambda e: self.cerrar_sesion(), height=20),
            ],
            content=ft.Row(
                [
                    ft.CircleAvatar(
                        content=ft.Image(src='/avatar.png',
                                         width=40, height=40),
                        radius=16,
                        bgcolor="#4A90E2",
                    ),
                    ft.Text(
                        user,
                        color=color_texto(),
                        size=14,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.END,

            ),
            menu_position=ft.PopupMenuPosition.UNDER,
            bgcolor=color_bg_2())

    # --- Crear las vistas ---
        view_reportes = VistaReportes(self.page, self.context).build()
        view_about = VistaAbout(self.page, self.context).build()
        view_permiso_operacion = VistaPermisoOperacion(
            self.page, self.context).build()
        # view_dashboard = VistaDashBoard(self.page, self.context).build()

        # --- Contenedor dinámico donde se cargan las vistas ---
        self.main_content = ft.Container(
            expand=1,
            content=view_reportes  # vista inicial
        )

    # --- Función para cambiar vista según selección ---
        def on_nav_change(e):
            index = e.control.selected_index
            if index == 0:
                self.main_content.content = view_reportes
            elif index == 1:
                self.main_content.content = view_reportes
            elif index == 2:
                self.main_content.content = view_permiso_operacion
            elif index == 3:
                self.main_content.content = view_about
            self.page.update()  # type: ignore

        # --- Menú lateral (NavigationRail) ---
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            indicator_color=bg_color,
            indicator_shape=ft.RoundedRectangleBorder(radius=5),
            selected_label_text_style=ft.TextStyle(),
            bgcolor=bg_2_color,
            leading=ft.Image(src="/saft.png", width=50),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.SPACE_DASHBOARD_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.SPACE_DASHBOARD_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Dashbord",  color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.VIEW_COMFORTABLE_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.VIEW_COMFORTABLE_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Reportes",  color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.ADD_HOME_WORK_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.ADD_HOME_WORK_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Permiso Operación.", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icon(ft.Icons.ARCHIVE_OUTLINED,
                                 color=text_color, size=20),
                    selected_icon=ft.Icon(
                        ft.Icons.ARCHIVE_ROUNDED, color=text_color, size=20),
                    label_content=ft.Text(
                        "Acerca De", color=text_color, size=11, text_align=ft.TextAlign.CENTER),
                    indicator_color=shadow_color,
                ),
            ],
            on_change=on_nav_change,
        )

        self.con_rail = create_container_rail(
            content=rail,
            expand=False
        )
        # --- Fondo principal ---
        self.page.bgcolor = bg_color

    def build(self):  # type: ignore
        # self.page.title = "Reportes SAFT"  # type: ignore

        return ft.Column(
            [
                ft.Row([self.titulo_muni, self.user_info],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row(
                    [
                        self.con_rail,
                        ft.VerticalDivider(width=2),
                        self.main_content,  # donde se muestran las vistas
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )

    def cerrar_sesion(self):
        self.page.window.close()
        self.page.window.destroy()  # Cierra la ventana completa
        os._exit(0)
