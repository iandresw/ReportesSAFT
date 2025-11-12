
import flet as ft
from ui.btn_actualizar import create_update_button
from helpers.updater_helper import descargar_actualizacion, reemplazar_archivos
from utils.utils import close_app, is_admin, is_app_running, leer_version_local, leer_version_remota
import os
import subprocess
EXE_NAME = "reportes_saft.exe"
APP_DIR = r"C:\Program Files (x86)\SAFT\reportes_py"


class VistaUpdater:
    def __init__(self, page: ft.Page):
        self.page = page

        self.title = ft.Text("Actualizador ReportesSAFT",
                             # style=ft.TextThemeStyle.HEADLINE_SMALL,
                             size=22,
                             weight=ft.FontWeight.BOLD,
                             color="#FFFFFF",
                             text_align=ft.TextAlign.CENTER
                             )
        self.progress = ft.ProgressRing(width=70, height=70, value=100)
        self.status = ft.Text("", size=16, text_align=ft.TextAlign.CENTER)
        self.close_button = ft.ElevatedButton(
            "Cerrar aplicación y continuar", icon=ft.Icons.CLOSE, visible=False, on_click=self.close_and_continue)
        self.start_button = create_update_button()
        self.start_button.on_click = self.start_update
        if not is_admin():
            self.status.value = "Sin permisos de administrador"

    def update_status(self, msg: str, busy=True):
        self.status.value = msg
        self.status.update()
        self.progress.visible = busy
        self.progress.update()

    def start_update(self, e=None):
        self.start_button.visible = False  # type: ignore
        self.progress.visible = True
        self.page.update()

        if is_app_running():
            self.update_status("La aplicación está abierta.")
            self.progress.visible = False
            self.close_button.visible = True
            self.page.update()
            return

        try:
            version_local = leer_version_local()
            version_remota = leer_version_remota()
            self.update_status(
                f"Versión local: {version_local}\nVersión remota: {version_remota}")
            if version_local == version_remota:
                self.update_status(
                    "Tu aplicación ya está actualizada.", busy=False)
                self.start_button.visible = True  # type: ignore
                self.page.update()
                return

            tmp_dir = descargar_actualizacion(self, )
            reemplazar_archivos(self,  tmp_dir)

            self.update_status(
                f"Actualizada a versión {version_remota}", busy=False)
            self.page.update()
            exe_path = os.path.join(APP_DIR, EXE_NAME)
            if os.path.exists(exe_path):
                self.update_status("Reiniciando aplicación...")
                subprocess.Popen([exe_path], shell=True)
        except Exception as ex:
            self.update_status(f"Error: {ex}", busy=False)
            self.start_button.visible = True
            self.page.update()

    def close_and_continue(self, e):
        self.update_status("Cerrando aplicación...")
        close_app()
        self.close_button.visible = False
        self.page.update()
        self.start_update()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    self.title,
                    self.progress,
                    self.status,
                    self.start_button,
                    self.close_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
