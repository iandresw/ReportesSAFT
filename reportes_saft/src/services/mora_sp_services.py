from repositories.facturas_repository import FacturasRepository
from repositories.cuenta_ingreso_repository import CuentaIngresoRepository
from services.parametro_service import ParametroService


class MoraSPService:
    def __init__(self, conexion, sistem):
        self.repo_factura = FacturasRepository(conexion)
        self.repo_cta_ingreso = CuentaIngresoRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem

    def obtener_mora_sp_sami(self):
        cta_agua = '152190201'
        cta_alcantarillado = '152190202'
        cta_tren_aseo = '152190205'
        cta_bomberos = '152190206'
        cta_limpieza_solares = '125990212'
        cta_aseo_parques = '125990108'
        cta_limpieza_cementerio = '125990213'
        cta_aseo_cementerio = '125990109'
        cta_ambiente = '125990105'
        cta_contribucion = '223101010'
        contado = 0
        datos_agua = []
        datos_alcantarillado = []
        datos_tren = []
        datos_bombero = []
        datos_solares = []
        datos_parques = []
        datos_lim_cementerio = []
        datos_ase_cementerio = []
        datos_ambiente = []
        datos_contribucuion = []

        data_cta_agua = self.repo_cta_ingreso.obtener_cta_sp(cta_agua)
        data_cta_alcantarillado = self.repo_cta_ingreso.obtener_cta_sp(
            cta_alcantarillado)
        data_cta_tren_aseo = self.repo_cta_ingreso.obtener_cta_sp(
            cta_tren_aseo)
        data_cta_bombero = self.repo_cta_ingreso.obtener_cta_sp(cta_bomberos)
        data_cta_solares = self.repo_cta_ingreso.obtener_cta_sp(
            cta_limpieza_solares)
        data_cta_parques = self.repo_cta_ingreso.obtener_cta_sp(
            cta_aseo_parques)
        data_cta_limpieza_cementerio = self.repo_cta_ingreso.obtener_cta_sp(
            cta_limpieza_cementerio)
        data_cta_aseo_cemenetrio = self.repo_cta_ingreso.obtener_cta_sp(
            cta_aseo_cementerio)
        data_cta_ambiente = self.repo_cta_ingreso.obtener_cta_sp(cta_ambiente)
        data_cta_contribucion = self.repo_cta_ingreso.obtener_cta_sp(
            cta_contribucion)
# MORA AGUA
        mora_agua = self.repo_factura.obtener_mora_sp(cta_agua)
        for mora in mora_agua:
            contado += 1
            datos_agua.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_agua:
            mora_agua = self.repo_factura.obtener_mora_sp(
                data_cta_agua['CtaRecuperacion'])
            for mora in mora_agua:
                contado += 1
                datos_agua.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_agua = self.repo_factura.obtener_mora_sp(
                data_cta_agua['CtaInteres'])
            for mora in mora_agua:
                contado += 1
                datos_agua.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_agua = self.repo_factura.obtener_mora_sp(
                data_cta_agua['CtaRecargos'])
            for mora in mora_agua:
                contado += 1
                datos_agua.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

# MORA ALCANTARILLADO
        mora_alcanta = self.repo_factura.obtener_mora_sp(cta_alcantarillado)
        for mora in mora_alcanta:
            contado += 1
            datos_alcantarillado.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_alcantarillado:
            mora_alcanta = self.repo_factura.obtener_mora_sp(
                data_cta_alcantarillado['CtaRecuperacion'])
            for mora in mora_alcanta:
                contado += 1
                datos_alcantarillado.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_alcanta = self.repo_factura.obtener_mora_sp(
                data_cta_alcantarillado['CtaInteres'])
            for mora in mora_alcanta:
                datos_alcantarillado.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_alcanta = self.repo_factura.obtener_mora_sp(
                data_cta_alcantarillado['CtaRecargos'])
            for mora in mora_alcanta:
                datos_alcantarillado.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

 # MORA TREN DE ASEO
        mora_tren_aseo = self.repo_factura.obtener_mora_sp(cta_tren_aseo)
        for mora in mora_tren_aseo:
            contado += 1
            datos_tren.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_tren_aseo:
            mora_tren_aseo = self.repo_factura.obtener_mora_sp(
                data_cta_tren_aseo['CtaRecuperacion'])
            for mora in mora_tren_aseo:
                contado += 1
                datos_tren.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_tren_aseo = self.repo_factura.obtener_mora_sp(
                data_cta_tren_aseo['CtaInteres'])
            for mora in mora_tren_aseo:
                contado += 1
                datos_tren.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_tren_aseo = self.repo_factura.obtener_mora_sp(
                data_cta_tren_aseo['CtaRecargos'])
            for mora in mora_tren_aseo:
                contado += 1
                datos_tren.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

# MORA BOMBEROS
        mora_bombero = self.repo_factura.obtener_mora_sp(cta_bomberos)
        for mora in mora_bombero:
            contado += 1
            datos_bombero.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_bombero:
            mora_bombero = self.repo_factura.obtener_mora_sp(
                data_cta_bombero['CtaRecuperacion'])
            for mora in mora_bombero:
                contado += 1
                datos_bombero.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_bombero = self.repo_factura.obtener_mora_sp(
                data_cta_bombero['CtaInteres'])
            for mora in mora_bombero:
                contado += 1
                datos_bombero.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })

            mora_bombero = self.repo_factura.obtener_mora_sp(
                data_cta_bombero['CtaRecargos'])
            for mora in mora_bombero:
                contado += 1
                datos_bombero.append({
                    'Cuenta': mora['CtaIngreso'],
                    'Tipo': mora['NombreCtaIngreso'],
                    'Valor': mora['valor']
                })
# MORA LIMPIEZA DE SOLARES BALDIOS

        mora_solares = self.repo_factura.obtener_mora_sp(cta_limpieza_solares)
        for mora in mora_solares:
            contado += 1
            datos_solares.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_solares:
            if not data_cta_solares['CtaRecuperacion'] == '':
                mora_solares = self.repo_factura.obtener_mora_sp(
                    data_cta_solares['CtaRecuperacion'])
                for mora in mora_solares:
                    contado += 1
                    datos_solares.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_solares['CtaInteres'] == '':
                mora_solares = self.repo_factura.obtener_mora_sp(
                    data_cta_solares['CtaInteres'])
                for mora in mora_solares:
                    contado += 1
                    datos_solares.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_solares['CtaRecargos'] == '':
                mora_solares = self.repo_factura.obtener_mora_sp(
                    data_cta_solares['CtaRecargos'])
                for mora in mora_solares:
                    contado += 1
                    datos_solares.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']})

# MORA LIMPIEZA DE PARQUES Y AVENIDAD
        mora_parques = self.repo_factura.obtener_mora_sp(cta_aseo_parques)
        for mora in mora_parques:
            contado += 1
            datos_parques.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_parques:
            if not data_cta_parques['CtaRecuperacion'] == '':
                mora_parques = self.repo_factura.obtener_mora_sp(
                    data_cta_parques['CtaRecuperacion'])
                for mora in mora_parques:
                    contado += 1
                    datos_parques.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_parques['CtaInteres'] == '':
                mora_parques = self.repo_factura.obtener_mora_sp(
                    data_cta_parques['CtaInteres'])
                for mora in mora_parques:
                    contado += 1
                    datos_parques.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_parques['CtaRecargos'] == '':
                mora_parques = self.repo_factura.obtener_mora_sp(
                    data_cta_parques['CtaRecargos'])
                for mora in mora_parques:
                    contado += 1
                    datos_parques.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']})

# MORA LIMPIEZA DE CEMENETRIO
        mora_lim_cementerio = self.repo_factura.obtener_mora_sp(
            cta_limpieza_cementerio)
        for mora in mora_lim_cementerio:
            contado += 1
            datos_lim_cementerio.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_limpieza_cementerio:
            if not data_cta_limpieza_cementerio['CtaRecuperacion'] == '':
                mora_lim_cementerio = self.repo_factura.obtener_mora_sp(
                    data_cta_limpieza_cementerio['CtaRecuperacion'])
                for mora in mora_lim_cementerio:
                    contado += 1
                    datos_lim_cementerio.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_limpieza_cementerio['CtaInteres'] == '':
                mora_lim_cementerio = self.repo_factura.obtener_mora_sp(
                    data_cta_limpieza_cementerio['CtaInteres'])
                for mora in mora_lim_cementerio:
                    contado += 1
                    datos_lim_cementerio.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_limpieza_cementerio['CtaRecargos'] == '':
                mora_lim_cementerio = self.repo_factura.obtener_mora_sp(
                    data_cta_limpieza_cementerio['CtaRecargos'])
                for mora in mora_lim_cementerio:
                    contado += 1
                    datos_lim_cementerio.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']})

# MORA ASEO DE CEMENETRIO
        mora_aseo_cementerio = self.repo_factura.obtener_mora_sp(
            cta_aseo_cementerio)
        for mora in mora_aseo_cementerio:
            contado += 1
            datos_ase_cementerio.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_aseo_cemenetrio:
            if not data_cta_aseo_cemenetrio['CtaRecuperacion'] == '':
                mora_aseo_cementerio = self.repo_factura.obtener_mora_sp(
                    data_cta_aseo_cemenetrio['CtaRecuperacion'])
                for mora in mora_aseo_cementerio:
                    contado += 1
                    datos_lim_cementerio.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_aseo_cemenetrio['CtaInteres'] == '':
                mora_aseo_cementerio = self.repo_factura.obtener_mora_sp(
                    data_cta_aseo_cemenetrio['CtaInteres'])
                for mora in mora_aseo_cementerio:
                    contado += 1
                    datos_ase_cementerio.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_aseo_cemenetrio['CtaRecargos'] == '':
                mora_aseo_cementerio = self.repo_factura.obtener_mora_sp(
                    data_cta_aseo_cemenetrio['CtaRecargos'])
                for mora in mora_aseo_cementerio:
                    contado += 1
                    datos_ase_cementerio.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']})


# MORA AMBIENTAL
        mora_ambiente = self.repo_factura.obtener_mora_sp(
            cta_ambiente)
        for mora in mora_ambiente:
            contado += 1
            datos_ambiente.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_ambiente:
            if not data_cta_ambiente['CtaRecuperacion'] == '':
                mora_ambiente = self.repo_factura.obtener_mora_sp(
                    data_cta_ambiente['CtaRecuperacion'])
                for mora in mora_ambiente:
                    contado += 1
                    datos_ambiente.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_ambiente['CtaInteres'] == '':
                mora_ambiente = self.repo_factura.obtener_mora_sp(
                    data_cta_ambiente['CtaInteres'])
                for mora in mora_ambiente:
                    contado += 1
                    datos_ambiente.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_ambiente['CtaRecargos'] == '':
                mora_ambiente = self.repo_factura.obtener_mora_sp(
                    data_cta_ambiente['CtaRecargos'])
                for mora in mora_ambiente:
                    contado += 1
                    datos_ambiente.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']})
# MORA CONTRIBUCION
        mora_contribucion = self.repo_factura.obtener_mora_sp(cta_contribucion)
        for mora in mora_contribucion:
            contado += 1
            datos_contribucuion.append({
                'Cuenta': mora['CtaIngreso'],
                'Tipo': mora['NombreCtaIngreso'],
                'Valor': mora['valor']
            })
        if data_cta_contribucion:
            if not data_cta_contribucion['CtaRecuperacion'] == '':
                mora_contribucion = self.repo_factura.obtener_mora_sp(
                    data_cta_contribucion['CtaRecuperacion'])
                for mora in mora_contribucion:
                    contado += 1
                    datos_contribucuion.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_contribucion['CtaInteres'] == '':
                mora_contribucion = self.repo_factura.obtener_mora_sp(
                    data_cta_contribucion['CtaInteres'])
                for mora in mora_contribucion:
                    contado += 1
                    datos_contribucuion.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']
                    })
            if not data_cta_contribucion['CtaRecargos'] == '':
                mora_contribucion = self.repo_factura.obtener_mora_sp(
                    data_cta_contribucion['CtaRecargos'])
                for mora in mora_contribucion:
                    contado += 1
                    datos_contribucuion.append({
                        'Cuenta': mora['CtaIngreso'],
                        'Tipo': mora['NombreCtaIngreso'],
                        'Valor': mora['valor']})

        if not contado != 0:
            raise ValueError("No se encontraron datos de mora de sp.")
        return datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques, datos_lim_cementerio, datos_ase_cementerio, datos_ambiente, datos_contribucuion
