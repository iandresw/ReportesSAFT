
import tempfile
import requests
import os
import time
import zipfile
import shutil
URL_ZIP = "https://drive.usercontent.google.com/download?id=1qdcEkhAj50oRiZFmVpd8r-xxSi4BYPP4&export=download&authuser=0&confirm=t&uuid=def8ece9-9390-480f-aae2-670319bc8bde&at=ALWLOp4HdS0S2XQ9A3FoGrbWnPfO%3A1762643228171"
APP_DIR = r"C:\Program Files (x86)\SAFT\reportes_py"
EXCLUDE = ["config.ini", "user_data", "updater"]


def descargar_actualizacion(instancia):
    tmp_dir = tempfile.mkdtemp(prefix="update_")
    zip_path = os.path.join(tmp_dir, "update.zip")
    instancia.update_status("Descargando nueva versión...")
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
                        instancia.progress.value = descargado / total
                        instancia.page.update()
    instancia.progress.value = None
    instancia.progress.update()

    instancia.update_status("Extrayendo archivos...")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(tmp_dir)
    time.sleep(0.5)
    return tmp_dir


def reemplazar_archivos(instancia, src_dir):
    instancia.update_status("Actualizando archivos...")
    instancia.progress.value = None
    instancia.progress.update()
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
                    print(f"Archivo en uso: {dst}, reintentando...")
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Error copiando {file}: {e}")
                    break

    instancia.update_status("Archivos actualizados correctamente.", busy=False)
