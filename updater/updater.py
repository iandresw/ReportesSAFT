import os
import zipfile
import requests
import tempfile
import shutil
import subprocess

# === CONFIGURACIÓN ===
URL_VERSION = "https://raw.githubusercontent.com/tuusuario/tu-repo/main/version.txt"
URL_ZIP = "https://github.com/tuusuario/tu-repo/releases/latest/download/reportes_saft.zip"
APP_DIR = os.path.join(os.path.dirname(__file__), "..",
                       "build", "windows", "reportes_saft")
EXCLUDE = ["config.ini", "user_data", "updater"]


def leer_version_local():
    path = os.path.join(APP_DIR, "version.txt")
    if not os.path.exists(path):
        return "0.0.0"
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def leer_version_remota():
    print("🔍 Consultando versión remota...")
    r = requests.get(URL_VERSION, timeout=10)
    r.raise_for_status()
    return r.text.strip()


def descargar_actualizacion():
    tmp_dir = tempfile.mkdtemp(prefix="update_")
    zip_path = os.path.join(tmp_dir, "update.zip")

    print("📦 Descargando nueva versión...")
    with requests.get(URL_ZIP, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(1024 * 256):
                f.write(chunk)

    print("✅ Descarga completa, extrayendo archivos...")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(tmp_dir)

    return tmp_dir


def reemplazar_archivos(src_dir):
    print("🔄 Actualizando archivos...")
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        dest_dir = os.path.join(APP_DIR, rel_path)
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            if any(ex in root for ex in EXCLUDE) or file in EXCLUDE:
                continue
            src = os.path.join(root, file)
            dst = os.path.join(dest_dir, file)
            shutil.copy2(src, dst)
    print("✅ Archivos actualizados correctamente")


def main():
    print("🚀 Iniciando actualizador...\n")

    version_local = leer_version_local()
    version_remota = leer_version_remota()

    print(f"Versión local: {version_local}")
    print(f"Versión remota: {version_remota}\n")

    if version_local == version_remota:
        print("✔ Tu aplicación ya está actualizada.")
        return

    tmp_dir = descargar_actualizacion()
    reemplazar_archivos(tmp_dir)

    with open(os.path.join(APP_DIR, "version.txt"), "w", encoding="utf-8") as f:
        f.write(version_remota)

    print(f"✅ Aplicación actualizada a la versión {version_remota}")

    exe_path = os.path.join(APP_DIR, "reportes_saft.exe")
    if os.path.exists(exe_path):
        print("🔁 Reiniciando aplicación...")
        subprocess.Popen([exe_path])
    else:
        print("⚠ No se encontró el ejecutable, verifique la ruta.")


if __name__ == "__main__":
    main()
