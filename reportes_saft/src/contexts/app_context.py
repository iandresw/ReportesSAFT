from database.conexion import ConexionBD


class AppContext:
    def __init__(self):
        self._conexion_saft = None
        self._conexion_bitacora = None

    def init_saft(self):
        if not self._conexion_saft:
            self._conexion_saft = ConexionBD('SAFT')

    def init_bitacora(self):
        if not self._conexion_bitacora:
            self._conexion_bitacora = ConexionBD('SAFTBIT')

    @property
    def conexion_saft(self):
        return self._conexion_saft

    @property
    def conexion_bitacora(self):
        return self._conexion_bitacora
