
import asyncio
import flet as ft
from ui.btn_actualizar import cerrar_app_boton, create_update_button
from ui.ui_colors import color_texto, color_bg, color_bg_2, color_texto_parrafo
from helpers.updater_helper import descargar_actualizacion, reemplazar_archivos
from utils.utils import close_app, close_updater, is_admin, is_app_running, leer_version_local, leer_version_remota
import os
import subprocess
EXE_NAME = "reportes_saft.exe"
APP_DIR = r"C:\Program Files (x86)\SAFT\reportes_py"


class VistaUpdater:
    def __init__(self, page: ft.Page):
        self.page = page
        self.text_color = color_texto()
        self.text_notas = color_texto_parrafo()
        self.imagen = ft.Image(src="/imagen.png", width=290)
        self.title = ft.Text("Actualizador ReportesSAFT",
                             # style=ft.TextThemeStyle.HEADLINE_SMALL,
                             size=22,
                             weight=ft.FontWeight.BOLD,
                             color=self.text_color,
                             text_align=ft.TextAlign.CENTER
                             )
        self.progress = ft.ProgressRing(
            width=70, height=70, value=100, color=self.text_color)
        self.status = ft.Text(
            "", size=16, text_align=ft.TextAlign.CENTER, color=self.text_notas)
        self.logos = ft.Row(
            [ft.Image("/saft.png", width=40),
             ft.Image("/logo_amhon.png", width=70)],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.close_button = cerrar_app_boton()
        self.close_button.on_click = self.close_and_continue
        self.close_button.visible = False

        self.close_button_actual = cerrar_app_boton()
        self.close_button_actual.on_click = self.close_updater_click
        self.close_button_actual.text = "Cerrar Actualizador"
        self.close_button_actual.visible = False

        self.start_button = create_update_button()
        self.start_button.on_click = self.start_update
        if not is_admin():
            self.status.value = "Sin permisos de administrador"

    def update_status(self, msg: str, busy=True):
        self.status.value = msg
        self.status.update()
        self.progress.visible = busy
        self.progress.update()
        self.page.update()

    async def run_in_thread(self, func, *args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    async def start_update(self, e=None):
        self.start_button.visible = False
        self.progress.visible = True
        self.page.update()

        if await self.run_in_thread(is_app_running):
            self.update_status("La aplicación está abierta.")
            await asyncio.sleep(0.5)
            self.progress.visible = False
            self.close_button.visible = True
            self.page.update()
            return

        try:
            version_local = await self.run_in_thread(leer_version_local)
            version_remota = await self.run_in_thread(leer_version_remota)
            self.update_status(
                f"Versión local: {version_local}\nVersión remota: {version_remota}")

            if version_local == version_remota:
                self.update_status(
                    "Tu aplicación ya está actualizada.", busy=False)
                await asyncio.sleep(0.5)
                self.start_button.visible = True
                self.page.update()
                return

            tmp_dir = await self.run_in_thread(descargar_actualizacion, self)
            await self.run_in_thread(reemplazar_archivos, self, tmp_dir)

            exe_path = os.path.join(APP_DIR, EXE_NAME)
            if os.path.exists(exe_path):
                self.update_status("Reiniciando aplicación...")
                await self.run_in_thread(subprocess.Popen, [exe_path], shell=True)
            self.update_status(
                f"Actualizada a versión {version_remota}", busy=False)
            self.close_button_actual.visible = True
            self.start_button.visible = False
            self.page.update()

        except Exception as ex:
            self.update_status(f"Error: {ex}", busy=False)
            self.start_button.visible = True
            self.page.update()

    async def close_and_continue(self, e):
        self.update_status("Cerrando aplicación...")
        await self.run_in_thread(close_app)
        self.close_button.visible = False
        self.page.update()
        await self.start_update()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [self.logos,
                    self.title,
                    self.progress,
                    self.status,
                    self.start_button,
                    self.close_button,
                    self.close_button_actual,
                    self.imagen
                 ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

    def close_updater_click(self, e):
        self.page.window.close()  # Cierra la ventana
        import sys
        sys.exit(0)               # Finaliza el proceso
