import subprocess
import sys
import os
import flet as ft
import time
import requests
import re
from version import APP_VERSION

URL_VERSION = "https://raw.githubusercontent.com/iandresw/ReportesSAFT/master/reportes_saft/src/version.py"


class UpdateService:
    def __init__(self, page: ft.Page):
        self.page = page

    def verificar_actualizacion(self, e):
        try:
            version_local = self.leer_version_local()
            version_remota = self.leer_version_remota()
            if not version_local == version_remota:
                base_dir = r"C:\Program Files (x86)\SAFT\reportes_py"
                updater_ui = os.path.join(base_dir, "updater.exe")

                if os.path.exists(updater_ui):
                    snackbar = ft.SnackBar(
                        ft.Text("Iniciando actualización..."), open=True)
                    self.page.open(snackbar)
                    self.page.update()
                    time.sleep(1)
                    subprocess.Popen([updater_ui], shell=True)
                    self.page.window.close()
                    sys.exit(0)
                else:
                    snackbar = ft.SnackBar(
                        ft.Text(f"⚠ No se encontró el actualizador.{updater_ui}"), open=True)
                    self.page.open(snackbar)
                    self.page.update()
            snackbar = ft.SnackBar(
                ft.Text(f"Ya cuenta con la ultima Version Disponible"), open=True)
            self.page.open(snackbar)
            self.page.update()

        except Exception as ex:
            snackbar = ft.SnackBar(ft.Text(f"❌ Error: {str(ex)}"), open=True)
            self.page.open(snackbar)
            self.page.update()

    def leer_version_remota(self):
        r = requests.get(URL_VERSION, timeout=10)
        r.raise_for_status()
        contenido = r.text
        match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', contenido)
        return match.group(1) if match else "0.0.0"

    def leer_version_local(self):
        return APP_VERSION
