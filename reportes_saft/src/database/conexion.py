import pyodbc
from dotenv import load_dotenv
from contextlib import contextmanager
import os
import time
load_dotenv()


class ConexionBD:
    def __init__(self, tipo_bd):
        self.tipo_bd = tipo_bd
        self.conexion = None
        self._conectar()

    def _conectar(self):
        if self.tipo_bd == 'SAFT':
            self.conexion = pyodbc.connect(
                f"DSN={os.getenv('DSN_SAFT')};UID={os.getenv('SQLSERVER_UID')};PWD={os.getenv('SQLSERVER_PWD')}",
                autocommit=True
            )
        elif self.tipo_bd == 'SAFTBIT':
            self.conexion = pyodbc.connect(
                f"DSN={os.getenv('DSN_SAFTBIT')};UID={os.getenv('SQLSERVER_UID')};PWD={os.getenv('SQLSERVER_PWD')}",
                autocommit=True
            )
        else:
            raise ValueError(
                f"Tipo de base de datos no válido: {self.tipo_bd}")

    def reconectar(self, intentos=3, espera=5):
        """Reintenta reconectar en caso de error."""
        for intento in range(1, intentos + 1):
            try:
                print(
                    f"Intentando reconectar a {self.tipo_bd} (Intento {intento}/{intentos})...")
                self._conectar()
                print(f"Reconectado a {self.tipo_bd} exitosamente.")
                return
            except Exception as e:
                print(f"Falló el intento {intento}: {e}")
                time.sleep(espera)
        raise ConnectionError(
            f"No se pudo reconectar a {self.tipo_bd} después de {intentos} intentos.")

    def obtener_cursor(self):
        if self.conexion:
            return self.conexion.cursor()
        else:
            raise ValueError("La conexión no está establecida.")

    def cerrar_conexion(self):
        if self.conexion:
            self.conexion.close()
            print(f"Conexión {self.tipo_bd} cerrada correctamente.")
        else:
            print("No hay conexión activa para cerrar.")

    @contextmanager
    def cursor(self):
        """Context manager para manejar cursores de forma segura."""
        cur = self.obtener_cursor()
        try:
            yield cur

        except (pyodbc.Error) as e:
            print(f"Error de conexión: {e}")
            self.conexion.rollback()
            self.reconectar()
            raise
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cur.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conexion:
            try:
                if exc_type is None:
                    self.conexion.commit()
                    print(
                        f"Commit realizado correctamente en {self.tipo_bd}")
                else:
                    self.conexion.rollback()
                    print(f"Rollback realizado en {self.tipo_bd}")
            finally:
                self.conexion.close()
                print(f"Conexión {self.tipo_bd} cerrada.")
