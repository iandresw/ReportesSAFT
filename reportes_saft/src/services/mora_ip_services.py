from repositories.facturas_repository import FacturasRepository
from repositories.cuenta_ingreso_repository import CuentaIngresoRepository
from services.parametro_service import ParametroService


class MoraIPService:
    def __init__(self, conexion, sistem):
        self.repo_factura = FacturasRepository(conexion)
        self.repo_cta_ingreso = CuentaIngresoRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def obtener_mora_ip(self):
        cta_ip = self.sys['CtaIngresoIP']
        datos = []
        data_cta_ip = self.repo_cta_ingreso.obtener_cuentas(cta_ip)

        mora_ip = self.repo_factura.obtener_mora_ip(data_cta_ip['CtaIngreso'])
        datos.append({
            'Cuenta': data_cta_ip['CtaIngreso'],
            'Tipo': 'Saldo Año Actual Impuesto Personal',
            'Valor': mora_ip['valor']
        })


# INTERESES
        interes_ip = self.repo_factura.obtener_int_rec_ip(
            data_cta_ip['CtaInteres'])
        datos.append({
            'Cuenta': data_cta_ip['CtaInteres'],
            'Tipo': 'Intereses Sobre Impuesto Personal',
            'Valor': interes_ip['valor']
        })

 # RECARGOS
        recargos_ip = self.repo_factura.obtener_int_rec_ip(
            data_cta_ip['CtaRecargos']
        )
        datos.append({
            'Cuenta': data_cta_ip['CtaRecargos'],
            'Tipo': 'Recargos Sobre Impuesto Personal',
            'Valor': recargos_ip['valor']
        })


# RECUPERACION
        recuperacion_ip = self.repo_factura.obtener_mora_ip(
            data_cta_ip['CtaRecuperacion']
        )
        datos.append({
            'Cuenta': data_cta_ip['CtaRecuperacion'],
            'Tipo': 'Recuperación de Saldos Sobre Impuesto Personal',
            'Valor': recuperacion_ip['valor']
        })

        if not datos:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos
