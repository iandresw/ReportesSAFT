import subprocess
import sys
import os
import flet as ft
import time


class UpdateService:
    def __init__(self, page: ft.Page):
        self.page = page

    def verificar_actualizacion(self, e):
        try:

            base_dir = r"C:\Program Files (x86)\SAFT\reportes_py"
            updater_ui = os.path.join(base_dir, "updater.exe")

            if os.path.exists(updater_ui):
                # Mostrar mensaje visual en la app
                snackbar = ft.SnackBar(
                    ft.Text("Iniciando actualización..."), open=True)
                self.page.open(snackbar)
                self.page.update()

                # Esperar un momento para que el usuario vea el mensaje
                time.sleep(1)

                # Ejecutar el actualizador
                subprocess.Popen([updater_ui], shell=True)

                # Cerrar esta aplicación
                self.page.window.close()  # Cierra ventana Flet
                sys.exit(0)
            else:
                snackbar = ft.SnackBar(
                    ft.Text(f"⚠ No se encontró el actualizador.{updater_ui}"), open=True)
                self.page.open(snackbar)
                self.page.update()

        except Exception as ex:
            snackbar = ft.SnackBar(ft.Text(f"❌ Error: {str(ex)}"), open=True)
            self.page.open(snackbar)
            self.page.update()
