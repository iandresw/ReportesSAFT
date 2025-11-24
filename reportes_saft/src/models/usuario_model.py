class Usuario:
    def __init__(self, username: str, usuarioNombre: str, identidad: str, nivel: str, permisos: dict):
        self.username = username
        self.nombre = usuarioNombre
        self.identidad = identidad
        self.nivel = nivel
        self.permisos = permisos

    def tiene_permiso(self, modulo: str) -> bool:
        """Verifica si tiene acceso al módulo"""
        return modulo in self.permisos

    def nivel_modulo(self, modulo: str):
        """Retorna el nivel que tiene en un módulo específico"""
        return self.permisos.get(modulo)
