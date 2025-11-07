from repositories.facturas_repository import FacturasRepository
from repositories.cuenta_ingreso_repository import CuentaIngresoRepository
from services.parametro_service import ParametroService


class MoraBIService:
    def __init__(self, conexion, sistem):
        self.repo_factura = FacturasRepository(conexion)
        self.repo_cta_ingreso = CuentaIngresoRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def obtener_mora_bi_sami(self):
        cta_bi_urbano = self.sys['CtaIngresoBiUrb']
        cta_bi_rural = self.sys['CtaIngresoBiRural']

        datos = []

        data_cta_urbano = self.repo_cta_ingreso.obtener_cuentas(cta_bi_urbano)
        data_cta_rural = self.repo_cta_ingreso.obtener_cuentas(cta_bi_rural)

        mora_urbano = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaIngreso'])
        datos.append({
            'Cuenta': data_cta_urbano['CtaIngreso'],
            'Tipo': 'Saldo Año Actual Impuesto Sobre Bienes Inmuebles Urbanos',
            'Valor': mora_urbano['valor']
        })

        mora_rural = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaIngreso'])
        datos.append({
            'Cuenta': data_cta_rural['CtaIngreso'],
            'Tipo': 'Saldo Año Actual Impuesto Sobre Bienes Inmuebles Rural',
            'Valor': mora_rural['valor']
        })

# INTERESES
        interes_bi_urbano = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaInteres'])
        datos.append({
            'Cuenta': data_cta_urbano['CtaInteres'],
            'Tipo': 'Intereses Sobre Bienes Inmuebles Urbanos',
            'Valor': interes_bi_urbano['valor']
        })

        interes_bi_rural = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaInteres'])
        datos.append({
            'Cuenta': data_cta_rural['CtaInteres'],
            'Tipo': 'Intereses Sobre Bienes Inmuebles Rural',
            'Valor': interes_bi_rural['valor']
        })

 # RECARGOS
        recargos_bi_urbanos = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaRecargos']
        )
        datos.append({
            'Cuenta': data_cta_urbano['CtaRecargos'],
            'Tipo': 'Recargos Sobre Bienes Inmuebles Urbanos',
            'Valor': recargos_bi_urbanos['valor']
        })

        recargos_bi_rurales = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaRecargos']
        )
        datos.append({
            'Cuenta': data_cta_rural['CtaRecargos'],
            'Tipo': 'Recargos Sobre Bienes Inmuebles Rurales',
            'Valor': recargos_bi_rurales['valor']
        })


# RECUPERACION
        recuperacion_bi_urb = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaRecuperacion']
        )
        datos.append({
            'Cuenta': data_cta_urbano['CtaRecuperacion'],
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Urbanos',
            'Valor': recuperacion_bi_urb['valor']
        })

        recuperacion_bi_ru = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaRecuperacion']
        )
        datos.append({
            'Cuenta': data_cta_rural['CtaRecuperacion'],
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Rural',
            'Valor': recuperacion_bi_ru['valor']
        })

        if not datos:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos

    def obtener_mora_bi_gob(self):
        cta_bi_urbano = self.sys['CtaIngresoBiUrb']
        cta_bi_rural = self.sys['CtaIngresoBiRural']
        cta_recargo_bi_impuesto = self.sys['CtaIngresoRecargoImp']
        cta_interes_bi_impuesto = self.sys['CtaIngresoIntImp']

        datos = []

        data_cta_urbano = self.repo_cta_ingreso.obtener_cuentas(cta_bi_urbano)
        data_cta_rural = self.repo_cta_ingreso.obtener_cuentas(cta_bi_rural)
        print(type(data_cta_rural))
        mora_urbano = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaIngreso'])
        datos.append({
            'Cuenta': data_cta_urbano['CtaIngreso'],
            'Tipo': 'Saldo Año Actual Impuesto Sobre Bienes Inmuebles Urbanos',
            'Valor': mora_urbano['valor']
        })

        mora_rural = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaIngreso'])
        datos.append({
            'Cuenta': data_cta_rural['CtaIngreso'],
            'Tipo': 'Saldo Año Actual Impuesto Sobre Bienes Inmuebles Rural',
            'Valor': mora_rural['valor']
        })

# INTERESES
        interes_bi_urbano = self.repo_factura.obtener_mora_bi(
            cta_interes_bi_impuesto)
        datos.append({
            'Cuenta': cta_interes_bi_impuesto,
            'Tipo': 'Intereses Sobre Bienes Inmuebles',
            'Valor': interes_bi_urbano['valor']
        })

 # RECARGOS
        recargos_bi_urbanos = self.repo_factura.obtener_mora_bi(
            cta_recargo_bi_impuesto
        )
        datos.append({
            'Cuenta': cta_recargo_bi_impuesto,
            'Tipo': 'Recargos Sobre Bienes Inmuebles',
            'Valor': recargos_bi_urbanos['valor']
        })

        # RECUPERACION
        recuperacion_bi_urb = self.repo_factura.obtener_mora_bi(
            data_cta_urbano['CtaRecuperacion']
        )
        datos.append({
            'Cuenta': data_cta_urbano['CtaRecuperacion'],
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Urbanos',
            'Valor': recuperacion_bi_urb['valor']
        })

        recuperacion_bi_ru = self.repo_factura.obtener_mora_bi(
            data_cta_rural['CtaRecuperacion']
        )
        datos.append({
            'Cuenta': data_cta_rural['CtaRecuperacion'],
            'Tipo': 'Recuperación de Saldos Sobre Bienes Inmuebles Rural',
            'Valor': recuperacion_bi_ru['valor']
        })

        if not datos:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos
