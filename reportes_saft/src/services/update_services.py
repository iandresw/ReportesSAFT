import subprocess
import sys
import os
import flet as ft


class UpdateService:
    def __init__(self, page: ft.Page):
        self.page = page

    def verificar_actualizacion(self, e):
        try:
            updater_ui = os.path.join(os.path.dirname(
                sys.executable), "updater", "ui_progress.exe")

            if os.path.exists(updater_ui):
                self.page.open(ft.SnackBar(
                    ft.Text("Iniciando actualización..."), open=True))
                self.page.update()
                subprocess.Popen([updater_ui])
                sys.exit(0)
            else:
                self.page.open(ft.SnackBar(
                    ft.Text("No se encontró el actualizador."), open=True))
                self.page.update()
        except Exception as ex:
            self.page.open(ft.SnackBar(
                ft.Text(f"Error: {str(ex)}"), open=True))
            self.page.update()
