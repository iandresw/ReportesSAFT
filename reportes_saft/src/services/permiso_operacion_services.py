from repositories.permiso_operacion_repository import PermisoOperacionReposirory
from models.tra_permop import Tra_PermOpe
from datetime import datetime


class PermisooperacionServices:
    def __init__(self, conexion, sistem) -> None:
        self.repo = PermisoOperacionReposirory(conexion=conexion)
        self.sys = sistem
        self.anio = datetime.now().year

    def crear_permiso_operacion(self, num_recibo: int) -> Tra_PermOpe:
        permiso: Tra_PermOpe
        existe = self.repo.existe_recibo(num_recibo=num_recibo)
        if existe:
            datos = self.repo.recargar_datos(num_recibo=num_recibo)
            if datos:
                permiso = Tra_PermOpe(NumRecibo=datos['NumRecibo'],
                                      Identidad=datos['Identidad'],
                                      Direccion=datos['Direccion'],
                                      idrepresentante=datos['IdRepresentante'],
                                      Negocio=datos['Negocio'],
                                      NoPermiso=datos['NoPermiso'],
                                      Periodo=datos['Periodo'],
                                      Propietario=datos['Propietario'],
                                      Ubicacion=datos['Ubicacion'],
                                      Actividad=datos['Actividad'],
                                      Observacion=datos['Observacion'],
                                      Fecha=datos['Fecha'],
                                      CodAldea=datos['CodAldea'],
                                      Usuario=datos['Usuario'],
                                      UsuarioMod=datos['UsuarioMod'],
                                      FirmaJ=datos['FirmaJ'],
                                      ClaveCatastro=datos['ClaveCatastro'],
                                      CodProfesion='',
                                      FechaNac=datos['FechaNac'],
                                      rtn=datos['rtn'],
                                      Telefono=datos['Telefono'])
        else:
            datos = self.repo.obtener_datos(num_recibo=num_recibo)
            num_permiso = self.repo.obtener_num_po()
            permiso = Tra_PermOpe(NumRecibo=datos['NumRecibo'],
                                  Identidad=datos['Identidad'],
                                  Direccion=datos['Direccion'],
                                  idrepresentante=datos['IdRepresentante'],
                                  Negocio=datos['Negocio'],
                                  NoPermiso=int(num_permiso["UltNumPO"])+1,
                                  Periodo=self.anio,
                                  Propietario=f"{datos['Pnombre']} {datos['SNombre']} {datos['PApellido']} {datos['SApellido']}",
                                  Ubicacion=datos['Direccion'],
                                  Actividad=datos['NombreCtaIngreso'],
                                  Observacion="2",
                                  Fecha=datetime.now(),
                                  CodAldea="",
                                  Usuario="",
                                  UsuarioMod="",
                                  FirmaJ="",
                                  ClaveCatastro=datos['ClaveCatastro'],
                                  CodProfesion="",
                                  FechaNac=datos['FechaNac'],
                                  rtn=datos['rtn'],
                                  Telefono=datos['Telefono'])

        return permiso  # type: ignore

    def guardar_perm_operacion(self, data: Tra_PermOpe):
        return self.repo.insertar_tra_perm_ope(data.NoPermiso, data.Periodo, data.Identidad, data.Negocio, data.Propietario,
                                               data.Ubicacion, data.Actividad, data.Observacion, data.Fecha, data.CodAldea, data.NumRecibo)

    def existe_po(self, num_recibo: int):
        return self.repo.existe_recibo(num_recibo=num_recibo)
