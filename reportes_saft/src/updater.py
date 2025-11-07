import os
import sys
import time
import zipfile
import shutil
import tempfile
import subprocess
import requests
import tkinter as tk
from tkinter import ttk, messagebox


def descargar_y_extraer(url_zip, destino, progreso):
    tmp_dir = tempfile.mkdtemp(prefix="update_")
    zip_path = os.path.join(tmp_dir, "update.zip")

    progreso["text"].set("Descargando actualización...")
    progreso["bar"]["value"] = 0
    progreso["ventana"].update()

    with requests.get(url_zip, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        descargado = 0

        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(1024 * 256):
                if chunk:
                    f.write(chunk)
                    descargado += len(chunk)
                    if total > 0:
                        progreso["bar"]["value"] = descargado / total * 100
                        progreso["ventana"].update()

    progreso["text"].set("Extrayendo archivos...")
    progreso["bar"]["value"] = 0
    progreso["ventana"].update()

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(tmp_dir)

    for root, dirs, files in os.walk(tmp_dir):
        rel = os.path.relpath(root, tmp_dir)
        dest_root = os.path.join(destino, rel) if rel != "." else destino
        os.makedirs(dest_root, exist_ok=True)
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(dest_root, f)
            if os.path.exists(dst):
                os.remove(dst)
            shutil.copy2(src, dst)

    progreso["text"].set("Actualización completada ✅")
    progreso["bar"]["value"] = 100
    progreso["ventana"].update()
    time.sleep(1)


def main():
    if len(sys.argv) < 4:
        print("Uso: updater.exe <url_zip> <carpeta_destino> <exe_nombre>")
        time.sleep(3)
        sys.exit(1)

    url_zip = sys.argv[1]
    destino = sys.argv[2]
    exe_nombre = sys.argv[3]

    ventana = tk.Tk()
    ventana.title("Actualizando aplicación...")
    ventana.geometry("400x120")
    ventana.resizable(False, False)

    texto = tk.StringVar(value="Preparando actualización...")
    label = ttk.Label(ventana, textvariable=texto)
    label.pack(pady=10)

    bar = ttk.Progressbar(ventana, length=350, mode="determinate")
    bar.pack(pady=10)

    progreso = {"ventana": ventana, "text": texto, "bar": bar}

    ventana.after(200, lambda: iniciar_descarga(
        url_zip, destino, exe_nombre, progreso))
    ventana.mainloop()


def iniciar_descarga(url_zip, destino, exe_nombre, progreso):
    try:
        descargar_y_extraer(url_zip, destino, progreso)
        exe_path = os.path.join(destino, exe_nombre)
        progreso["text"].set("Reiniciando aplicación...")
        progreso["ventana"].update()
        time.sleep(1)
        subprocess.Popen([exe_path], close_fds=True)
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    finally:
        progreso["ventana"].destroy()
        sys.exit(0)


if __name__ == "__main__":
    main()
