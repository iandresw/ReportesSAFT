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

    def obtener_datos_usuario(self, usuario) -> Usuario | None:
        cursor = self.conexion.obtener_cursor()
        query = f"""
        SELECT 
            u.UsuarioNombre, 
            u.Identidad, 
            um.ModuloCod, 
            um.UMLevel
        FROM Usuario u
        INNER JOIN UsuarioModulo um ON u.UsuarioCod = um.UsuarioCod
        WHERE u.UsuarioCod = ?
        """
        cursor.execute(query, usuario)
        resultado = cursor.fetchall()
        if not resultado:
            return None
        return resultado
