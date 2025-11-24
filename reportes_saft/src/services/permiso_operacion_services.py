from repositories.permiso_operacion_repository import PermisoOperacionReposirory
from models.tra_permop import Tra_PermOpe
from datetime import datetime


class PermisooperacionServices:
    def __init__(self, appContext, sistem) -> None:
        self.conexion = appContext.conexion_saft
        self.user = appContext.usuario_actual
        self.repo = PermisoOperacionReposirory(conexion=self.conexion)
        self.sys = sistem
        self.anio = datetime.now().year

    def crear_permiso_operacion(self, num_recibo: int, justicia, tipo_per) -> Tra_PermOpe | None:
        permiso: Tra_PermOpe
        existe = self.repo.existe_recibo(num_recibo=num_recibo)
        if existe:
            datos = self.repo.recargar_datos(num_recibo=num_recibo)
            if datos:
                inicio_operacion = datos['FechaNac']
                if isinstance(inicio_operacion, datetime):
                    anio = inicio_operacion.year
                    if not anio == datos['Periodo']:
                        num_renovacion = int(datos['Periodo'])-anio
                    else:
                        num_renovacion = 1
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
                                      CodProfesion=self.tipo_cuenta(
                                          datos['CodProfesion']),
                                      FechaNac=datos['FechaNac'],
                                      rtn=datos['rtn'],
                                      Telefono=datos['Telefono'],
                                      NumeroRenovacion=num_renovacion)
        else:
            observ = "Apertura"
            datos = self.repo.obtener_datos(num_recibo=num_recibo)
            if not datos:
                return None
            inicio_operacion = datos['FechaNac']
            if isinstance(inicio_operacion, datetime):
                anio = inicio_operacion.year
                if not anio == datos['UltPeriodoFact']:
                    observ = "Renovacion"
                    num_renovacion = datos['UltPeriodoFact']-anio
                else:
                    num_renovacion = 1
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
                                  Observacion=observ,
                                  Fecha=datetime.now(),
                                  CodAldea=datos['CodAldea'],
                                  Usuario=self.user.username,
                                  UsuarioMod="",
                                  FirmaJ=justicia,
                                  ClaveCatastro=datos['ClaveCatastro'],
                                  CodProfesion=self.tipo_cuenta(
                datos['CodProfesion']),
                FechaNac=datos['FechaNac'],
                rtn=datos['rtn'],
                Telefono=datos['Telefono'],
                NumeroRenovacion=num_renovacion)
        return permiso  # type: ignore

    def guardar_perm_operacion(self, data: Tra_PermOpe):
        return self.repo.insertar_tra_perm_ope(data.NoPermiso, data.Periodo, data.Identidad, data.Negocio, data.Propietario,
                                               data.Ubicacion, data.Actividad, data.Observacion, data.Fecha, data.CodAldea, data.NumRecibo, data.FirmaJ, data.Usuario)

    def existe_po(self, num_recibo: int):
        return self.repo.existe_recibo(num_recibo=num_recibo)

    def tipo_cuenta(self, cta_ingreso: str):
        cta = cta_ingreso[:6]
        if cta in "117101" or cta in "111112":
            TipoCuenta = "Establecimiento Industrial"
        elif cta in "117102" or cta in "111113":
            TipoCuenta = "Establecimiento Comercial"
        elif cta in "117103" or cta in "111114":
            TipoCuenta = "Establecimiento de Servicio"
        else:
            TipoCuenta = "Establecimiento No Clasificado"
        return TipoCuenta
