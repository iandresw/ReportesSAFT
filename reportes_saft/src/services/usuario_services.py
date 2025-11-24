from repositories.usuario_repository import UsuarioRepository, Usuario
from utils.encriptador import ms_encrypt


class UsuarioService:
    def __init__(self, conexion):
        self.repo = UsuarioRepository(conexion)

    def login(self, usuario: str, password: str) -> bool:
        clave = ms_encrypt(password, "M1")
        datos_usuario = self.repo.get_usuario_por_credenciales(usuario, clave)
        return datos_usuario

    def obtener_datos_usuario(self, usuario) -> Usuario | None:
        accesos = self.repo.obtener_datos_usuario(usuario)
        if not accesos:
            return None
        permisos = {modulo: nivel for _, _, modulo, nivel in accesos}
        nombre = accesos[0][0]
        identidad = accesos[0][1]
        return Usuario(
            username=usuario.upper(),
            usuarioNombre=nombre,
            identidad=identidad,
            nivel=max(permisos.values()),
            permisos=permisos
        )
