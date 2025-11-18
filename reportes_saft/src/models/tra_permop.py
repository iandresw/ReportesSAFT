from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tra_PermOpe:
    NumRecibo: int
    Identidad: str
    Direccion: str
    idrepresentante: str
    Negocio: str
    NoPermiso: int
    Periodo: int
    Propietario: str
    Ubicacion: str
    Actividad: str
    Observacion: str
    Fecha: datetime
    CodAldea: str
    Usuario: str
    UsuarioMod: str
    FirmaJ: str
    ClaveCatastro: str
    CodProfesion: str
    FechaNac: datetime
    rtn: str
    Telefono: str
    NumeroRenovacion: int
