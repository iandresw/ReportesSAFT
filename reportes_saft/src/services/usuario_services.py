from repositories.usuario_repository import UsuarioRepository, Usuario
from utils.encriptador import ms_encrypt


class UsuarioService:
    def __init__(self, conexion):
        self.repo = UsuarioRepository(conexion)

    def login(self, usuario: str, password: str) -> bool:
        clave = ms_encrypt(password, "M1")
        datos_usuario = self.repo.get_usuario_por_credenciales(usuario, clave)
        return datos_usuario
