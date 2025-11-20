from models.usuario_model import Usuario


class UsuarioRepository():
    def __init__(self, conexion):
        self.conexion = conexion

    def get_usuario_por_credenciales(self, usuario, password):
        cursor = self.conexion.obtener_cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Usuario WHERE UsuarioCod = ? AND UsuarioPass = ?", (usuario, password))
        resultado = cursor.fetchone()
        return resultado[0] > 0
