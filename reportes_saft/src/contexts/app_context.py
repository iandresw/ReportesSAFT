from database.conexion import ConexionBD
from models.usuario_model import Usuario
from services.usuario_services import UsuarioService
import logging
from utils.logger_config import configurar_logger


class AppContext:
    def __init__(self):
        self._conexion_saft = None
        self._conexion_bitacora = None
        self._auth_service = None
        self.usuario_actual: Usuario = None  # type: ignore
        self.cod_muni = None
        self.logger = configurar_logger(
            nombre_app="saft_app_bd",
            nivel=logging.INFO
        )

    def init_saft(self):
        if not self._conexion_saft:
            self._conexion_saft = ConexionBD('SAFT', self.logger)
            self._auth_service = UsuarioService(self._conexion_saft)

    def init_bitacora(self):
        if not self._conexion_bitacora:
            self._conexion_bitacora = ConexionBD('SAFTBIT', self.logger)

    def init_services(self):
        self._conexion = ConexionBD('SAFT', self.logger)
        self._auth_service = UsuarioService(self._conexion)

    @property
    def conexion_saft(self):
        return self._conexion_saft

    @property
    def conexion_bitacora(self):
        return self._conexion_bitacora

    @property
    def auth_service(self):
        return self._auth_service
