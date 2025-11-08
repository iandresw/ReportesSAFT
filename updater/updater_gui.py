import os
import shlex
import sys
import re
import zipfile
import tempfile
import shutil
import requests
import subprocess
import ctypes
import flet as ft
import time
# === CONFIGURACIÓN ===
URL_VERSION = "https://raw.githubusercontent.com/iandresw/ReportesSAFT/master/reportes_saft/src/version.py"
URL_ZIP = "https://raw.githubusercontent.com/iandresw/ReportesSAFT/22f4c721e4d88d0133bec3334ce8f97756e941d7/releases/latest/download/reportes_saft.zip"
APP_DIR = r"C:\Program Files (x86)\SAFT\reportes_py"
EXE_NAME = "reportes_saft.exe"
VERSION_FILE = os.path.join(APP_DIR, "version.py")
EXCLUDE = ["config.ini", "user_data", "updater"]


# === FUNCIONES DE APOYO ===

def is_admin():
    """Verifica si el programa se está ejecutando con privilegios de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def leer_version_local():
    if not os.path.exists(VERSION_FILE):
        return "0.0.0"
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        contenido = f.read()
    match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', contenido)
    return match.group(1) if match else "0.0.0"


def leer_version_remota():
    r = requests.get(URL_VERSION, timeout=10)
    r.raise_for_status()
    contenido = r.text
    match = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', contenido)
    return match.group(1) if match else "0.0.0"


def is_app_running():
    """Verifica si reportes_saft.exe está en ejecución."""
    result = subprocess.run("tasklist", capture_output=True, text=True)
    return EXE_NAME.lower() in result.stdout.lower()


def close_app():
    """Cierra reportes_saft.exe si está abierta."""
    subprocess.run(["taskkill", "/f", "/im", EXE_NAME],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def create_update_button(on_click=None):
    return ft.Container(
        border=ft.Border(
            top=ft.BorderSide(2, ft.Colors.BLUE_700),
            right=ft.BorderSide(2, ft.Colors.BLUE_700),
            left=ft.BorderSide(2, ft.Colors.BLUE_700),
            bottom=ft.BorderSide(2, ft.Colors.BLUE_700),
        ),
        border_radius=18,
        content=ft.ElevatedButton(
            text="Actualizar aplicación",
            icon=ft.Icons.SYSTEM_UPDATE,
            color=ft.Colors.BLUE_700,
            width=200,
            style=ft.ButtonStyle(
                bgcolor='#1b263b',
                shadow_color='#E06C75',
                text_style=ft.TextStyle(
                    size=10,
                    italic=False,
                    font_family="Tahoma",
                ),
                alignment=ft.Alignment(0, 0),
            ),
            on_click=on_click
        )
    )


# === INTERFAZ FLET ===

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

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    title = ft.Text("🔄 Actualizador ReportesSAFT", size=22,
                    weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    progress = ft.ProgressRing(width=70, height=70)
    status = ft.Text("", size=16, text_align=ft.TextAlign.CENTER)

    # Mostrar estado inicial según permisos
    if is_admin():
        status.value = "✅ Ejecutando como administrador"
    else:
        status.value = "⚠ Sin permisos de administrador"

    close_button = ft.ElevatedButton(
        "Cerrar aplicación y continuar", icon=ft.Icons.CLOSE, visible=False)

    def update_status(msg: str, busy=True):
        status.value = msg
        progress.visible = busy
        page.update()

    def descargar_actualizacion():
        tmp_dir = tempfile.mkdtemp(prefix="update_")
        zip_path = os.path.join(tmp_dir, "update.zip")
        update_status("Descargando nueva versión...")
        with requests.get(URL_ZIP, stream=True, timeout=60) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            descargado = 0
            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(1024 * 256):
                    if chunk:
                        f.write(chunk)
                        descargado += len(chunk)
                        if total:
                            progress.value = descargado / total
                            page.update()

        update_status("Extrayendo archivos...")

        # Extraer y cerrar correctamente el ZIP
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(tmp_dir)

        # Esperar brevemente para liberar el archivo
        time.sleep(0.5)

        return tmp_dir

    def reemplazar_archivos(src_dir):
        update_status("Actualizando archivos...")

        for root, dirs, files in os.walk(src_dir):
            rel_path = os.path.relpath(root, src_dir)
            dest_dir = os.path.join(APP_DIR, rel_path)
            os.makedirs(dest_dir, exist_ok=True)

            for file in files:
                if any(ex in root for ex in EXCLUDE) or file in EXCLUDE:
                    continue

                src = os.path.join(root, file)
                dst = os.path.join(dest_dir, file)

                # Reintentos si el archivo está bloqueado
                for intento in range(5):
                    try:
                        shutil.copy2(src, dst)
                        break
                    except PermissionError:
                        print(f"⚠ Archivo en uso: {dst}, reintentando...")
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"❌ Error copiando {file}: {e}")
                        break

        update_status("✅ Archivos actualizados correctamente.", busy=False)

    def start_update(e=None):
        start_button.visible = False
        progress.visible = True
        page.update()

        if is_app_running():
            update_status("⚠ La aplicación está abierta.")
            progress.visible = False
            close_button.visible = True
            page.update()
            return

        try:
            version_local = leer_version_local()
            version_remota = leer_version_remota()
            update_status(
                f"Versión local: {version_local}\nVersión remota: {version_remota}")
            if version_local == version_remota:
                update_status(
                    "✔ Tu aplicación ya está actualizada.", busy=False)
                start_button.visible = True
                page.update()
                return

            tmp_dir = descargar_actualizacion()
            reemplazar_archivos(tmp_dir)

            update_status(
                f"✅ Actualizada a versión {version_remota}", busy=False)
            page.update()
            exe_path = os.path.join(APP_DIR, EXE_NAME)
            if os.path.exists(exe_path):
                update_status("🔁 Reiniciando aplicación...")
                subprocess.Popen([exe_path], shell=True)
        except Exception as ex:
            update_status(f"❌ Error: {ex}", busy=False)
            start_button.visible = True
            page.update()

    def close_and_continue(e):
        update_status("Cerrando aplicación...")
        close_app()
        close_button.visible = False
        page.update()
        start_update()

    start_button = create_update_button(start_update)
    close_button.on_click = close_and_continue

    page.add(
        ft.Column(
            [title, progress, status, start_button, close_button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )


# === PUNTO DE ENTRADA ===
if __name__ == "__main__":
    # 1️⃣ Verificar si ya tenemos permisos de administrador
    if not is_admin():
        if "--elevated" not in sys.argv:
            import shlex

            # Ruta completa del script actual (funciona tanto en .py como .exe)
            if getattr(sys, 'frozen', False):
                # ejecutable empaquetado (.exe)
                script_path = sys.executable
            else:
                # script Python normal
                script_path = os.path.abspath(sys.argv[0])

            # Construir argumentos
            args = [script_path] + sys.argv[1:] + ["--elevated"]
            try:
                params = shlex.join(args)
            except AttributeError:
                params = " ".join(f'"{a}"' for a in args)

            print("🔒 Solicitando permisos de administrador...")
            hinstance = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            if int(hinstance) > 32:
                sys.exit(0)
            else:
                print("❌ No se concedieron permisos de administrador.")
                sys.exit(1)

    # 2️⃣ Si llegamos aquí, ya tenemos permisos de admin
    print("✅ Ejecutando como administrador...")

    # 3️⃣ Iniciar la app Flet normalmente
    ft.app(target=main)
