import ctypes
import os
import requests
import subprocess
import re
URL_VERSION = "https://raw.githubusercontent.com/iandresw/ReportesSAFT/master/reportes_saft/src/version.py"
URL_ZIP = "https://drive.usercontent.google.com/download?id=1qdcEkhAj50oRiZFmVpd8r-xxSi4BYPP4&export=download&authuser=0&confirm=t&uuid=def8ece9-9390-480f-aae2-670319bc8bde&at=ALWLOp4HdS0S2XQ9A3FoGrbWnPfO%3A1762643228171"
APP_DIR = r"C:\Program Files (x86)\SAFT\reportes_py"
VERSION_FILE = os.path.join(APP_DIR, "version.py")
EXE_NAME = "reportes_saft.exe"


def is_admin():
    """Verifica si el programa se está ejecutando con privilegios de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def leer_version_local():
    if not os.path.exists(VERSION_FILE):
        r = requests.get(URL_VERSION, timeout=10)
        r.raise_for_status()
        contenido = r.text
        match = re.search(
            r'APP_VERSION_LOCAL\s*=\s*["\']([^"\']+)["\']', contenido)
        return match.group(1) if match else "0.0.0"
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
