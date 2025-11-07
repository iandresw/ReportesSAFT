from repositories.facturas_repository import FacturasRepository
from repositories.cuenta_ingreso_repository import CuentaIngresoRepository
from services.parametro_service import ParametroService


class MoraICSService:
    def __init__(self, conexion, sistem):
        self.repo_factura = FacturasRepository(conexion)
        self.repo_cta_ingreso = CuentaIngresoRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def obtener_mora_ics_sami(self):
        cta_idustria = '117101'
        cta_comercio = '117102'
        cta_servicio = '117103'
        cta_rotulo = '125990205'
        cta_multa_declacion = self.sys['CtaIngresoMultaDeclaraTarde']
        cta_multa_operacion = self.sys['CtaIngresoMultaOPSinPermiso']

        datos_i = []
        datos_c = []
        datos_s = []
        datos_t = []

        data_cta_industria = self.repo_cta_ingreso.obtener_cuentas_ics(
            cta_idustria)
        data_cta_comercio = self.repo_cta_ingreso.obtener_cuentas_ics(
            cta_comercio)
        data_cta_servicio = self.repo_cta_ingreso.obtener_cuentas_ics(
            cta_servicio)

        mora_industria = self.repo_factura.obtener_mora_ics(cta_idustria)
        for mora in mora_industria:
            datos_i.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        mora_comercio = self.repo_factura.obtener_mora_ics(cta_comercio)
        for mora in mora_comercio:
            datos_c.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        mora_servicio = self.repo_factura.obtener_mora_ics(cta_servicio)
        for mora in mora_servicio:
            datos_s.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })


# INTERESES
        interes_industria = self.repo_factura.obtener_interes_ics(
            data_cta_industria['CtaInteres'])
        for mora in interes_industria:
            datos_i.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        interes_comercio = self.repo_factura.obtener_interes_ics(
            data_cta_comercio['CtaInteres'])
        for mora in interes_comercio:
            datos_c.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        interes_servicio = self.repo_factura.obtener_interes_ics(
            data_cta_servicio['CtaInteres'])
        for mora in interes_servicio:
            datos_s.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

 # RECARGOS
        recargo_industria = self.repo_factura.obtener_interes_ics(
            data_cta_industria['CtaRecargos'])
        for mora in recargo_industria:
            datos_i.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        recargo_comercio = self.repo_factura.obtener_interes_ics(
            data_cta_comercio['CtaRecargos'])
        for mora in recargo_comercio:
            datos_c.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        recargo_servicio = self.repo_factura.obtener_interes_ics(
            data_cta_servicio['CtaRecargos'])
        for mora in recargo_servicio:
            datos_s.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
# RECUPERACION
        recuperacion_industria = self.repo_factura.obtener_interes_ics(
            data_cta_industria['CtaRecuperacion'])
        for mora in recuperacion_industria:
            datos_i.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        recuperacion_comercio = self.repo_factura.obtener_interes_ics(
            data_cta_comercio['CtaRecuperacion'])
        for mora in recuperacion_comercio:
            datos_c.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        recuperacion_servicio = self.repo_factura.obtener_interes_ics(
            data_cta_servicio['CtaRecuperacion'])
        for mora in recuperacion_servicio:
            datos_s.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
# MULTAS
        multa_opreacion = self.repo_factura.obtener_interes_ics(
            cta_multa_operacion)
        for mora in multa_opreacion:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        multa_declaracion = self.repo_factura.obtener_interes_ics(
            cta_multa_declacion)
        for mora in multa_declaracion:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        rotulos = self.repo_factura.obtener_tasas_ics(
            cta_rotulo)
        for mora in rotulos:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        if not datos_c:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos_i, datos_c, datos_s, datos_t
        if not datos_c:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos_i, datos_c, datos_s, datos_t

    def obtener_mora_ics_gob(self):
        cta_idustria = '111112'
        cta_comercio = '111113'
        cta_servicio = '111114'
        cta_multa_declacion = self.sys['CtaIngresoMultaDeclaraTarde']
        cta_multa_operacion = self.sys['CtaIngresoMultaOPSinPermiso']
        cta_rotulo = '11111814'
        cta_interes = self.sys['CtaIngresoIntImp']
        cta_recargo = self.sys['CtaIngresoRecargoImp']

        datos_i = []
        datos_c = []
        datos_s = []
        datos_t = []

        data_cta_industria = self.repo_cta_ingreso.obtener_cuentas_ics(
            cta_idustria)
        data_cta_comercio = self.repo_cta_ingreso.obtener_cuentas_ics(
            cta_comercio)
        data_cta_servicio = self.repo_cta_ingreso.obtener_cuentas_ics(
            cta_servicio)

        cta_recuperacion_i = data_cta_industria['CtaRecuperacion']
        cta_recuperacion_c = data_cta_comercio['CtaRecuperacion']
        cta_recuperacion_s = data_cta_servicio['CtaRecuperacion']

        mora_industria = self.repo_factura.obtener_mora_ics(cta_idustria)
        for mora in mora_industria:
            datos_i.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        mora_comercio = self.repo_factura.obtener_mora_ics(cta_comercio)
        for mora in mora_comercio:
            datos_c.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        mora_servicio = self.repo_factura.obtener_mora_ics(cta_servicio)
        for mora in mora_servicio:
            datos_s.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })


# INTERESES

        interes_ics = self.repo_factura.obtener_interes_ics(cta_interes)
        for mora in interes_ics:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

 # RECARGOS
        recargo_ics = self.repo_factura.obtener_interes_ics(cta_recargo)
        for mora in recargo_ics:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
# RECUPERACION
        recuperacion_industria = self.repo_factura.obtener_interes_ics(
            cta_recuperacion_i)
        for mora in recuperacion_industria:
            datos_i.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        recuperacion_comercio = self.repo_factura.obtener_interes_ics(
            cta_recuperacion_c)
        for mora in recuperacion_comercio:
            datos_c.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        recuperacion_servicio = self.repo_factura.obtener_interes_ics(
            cta_recuperacion_s)
        for mora in recuperacion_servicio:
            datos_s.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
# MULTAS
        multa_opreacion = self.repo_factura.obtener_interes_ics(
            cta_multa_operacion)
        for mora in multa_opreacion:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        multa_declaracion = self.repo_factura.obtener_interes_ics(
            cta_multa_declacion)
        for mora in multa_declaracion:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

# ROTULOS
        rotulos = self.repo_factura.obtener_interes_ics(cta_rotulo)
        for mora in rotulos:
            datos_t.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })

        if not datos_c:
            raise ValueError("No se encontraron datos de mora BI.")
        return datos_i, datos_c, datos_s, datos_t
