from storage.data.conexion import ConexionBD


class AppContext:
    def __init__(self):
        self._conexion_saft = None
        self._conexion_bitacora = None
        self._auth_service = None
        self.usuario_actual: Usuario = None  # type: ignore
        self.cod_muni = None

    def init_saft(self):
        if not self._conexion_saft:
            self._conexion_saft = ConexionBD('SAFT')

    def init_bitacora(self):
        if not self._conexion_bitacora:
            self._conexion_bitacora = ConexionBD('SAFTBIT')

    def init_services(self):
        self._conexion = ConexionBD('SAFT')

    @property
    def conexion_saft(self):
        return self._conexion_saft

    @property
    def conexion_bitacora(self):
        return self._conexion_bitacora
