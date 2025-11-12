import os
import shlex
import sys
import ctypes
import flet as ft
from views.updater_view import VistaUpdater
from utils.utils import is_admin
from dotenv import load_dotenv
# === CONFIGURACIÓN ===
APP_DIR = r"C:\Program Files (x86)\SAFT\reportes_py"
load_dotenv()


def main(page: ft.Page):
    page.title = "Actualizador ReportesSAFT"
    x_width = 350
    x_height = 700
    page.bgcolor = '#1b263b'
    page.window.width = x_width
    page.window.height = x_height
    page.window.max_height = x_height
    page.window.min_height = x_height
    page.window.max_width = x_width
    page.window.min_width = x_width
    vista_updater = VistaUpdater(page).build()
    page.add(vista_updater)


# === PUNTO DE ENTRADA ===
if __name__ == "__main__":
    print(os.getenv("DEBUG_SKIP_ELEVATE"))
    if not os.getenv("DEBUG_SKIP_ELEVATE") == "1":
        if not is_admin():
            if "--elevated" not in sys.argv:
                if getattr(sys, 'frozen', False):
                    script_path = sys.executable
                else:
                    script_path = os.path.abspath(sys.argv[0])
                args = [script_path] + sys.argv[1:] + ["--elevated"]
                try:
                    params = shlex.join(args)
                except AttributeError:
                    params = " ".join(f'"{a}"' for a in args)
                    hinstance = ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, params, None, 1)
                    if int(hinstance) > 32:
                        sys.exit(0)
                    else:
                        sys.exit(1)
    ft.app(target=main)
