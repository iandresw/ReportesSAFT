import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CRED_FILE = os.path.join(BASE_DIR, "database", "credenciales.json")


class ManejadorCredenciales:
    @staticmethod
    def guardar(usuario: str, password: str):
        with open(CRED_FILE, "w", encoding="utf-8") as f:
            json.dump({"usuario": usuario, "password": password}, f)

    @staticmethod
    def cargar() -> dict:
        if os.path.exists(CRED_FILE):
            with open(CRED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"usuario": "", "password": ""}

    @staticmethod
    def borrar():
        if os.path.exists(CRED_FILE):
            os.remove(CRED_FILE)
