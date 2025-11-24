from datetime import datetime
from repositories.trancicion_ip_repository import TrancicionIPRepository
from repositories.trancicion_bi_repository import TrancicionBIRepository
from repositories.trancicion_ics_repository import TrancicionICSRepository
from repositories.trancicion_amb_reposiory import TrancicionAMBRepository
import pandas as pd
from repositories.trancicion_ps_reposiory import TrancicionSPRepository
from repositories.aldea_repository import AldeaRepository
from services.parametro_service import ParametroService


class TrancicionTraspasoService:
    def __init__(self, conexion, sistem):
        self.repo_trancicion_ip = TrancicionIPRepository(conexion)
        self.repo_trancicion_bi = TrancicionBIRepository(conexion)
        self.repo_trancicion_ics = TrancicionICSRepository(conexion)
        self.repo_trancicion_sp = TrancicionSPRepository(conexion)
        self.repo_trancicion_amb = TrancicionAMBRepository(conexion)
        self.repo_aldea = AldeaRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem
        self.codAldea = self.repo_aldea.obtener_aldea_urbana()
        self.anio = datetime.now().year

    def obtener_contribuyentes(self):
        data = []
        data_catastro = []
        aldea = self.codAldea['CodAldea']
        propiedades_urbano = self.repo_trancicion_bi.obtener_bi_urbano()
        propiedades_rural = self.repo_trancicion_bi.obtener_bi_rural()
        propiedades_urbano_act = self.repo_trancicion_bi.obtener_bi_urbano_activos(
            self.anio)
        propiedades_rural_act = self.repo_trancicion_bi.obtener_bi_rural_activos(
            self.anio)

        data.append({
            'Tipo': 'Bienes Inmuebles',
            'Valor_ins_urb': propiedades_urbano['Total'] or 0,
            'Valor_ins_rur': propiedades_rural['Total'] or 0,
            'Valor_act_urb': propiedades_urbano_act['Total'] or 0,
            'Valor_act_rur': propiedades_rural_act['Total'] or 0,
        })

        cta_ip = self.sys['CtaIngresoIP']
        personal_urbano_d = self.repo_trancicion_ip.obtener_ip_urbano(aldea)
        personal_rural_d = self.repo_trancicion_ip.obtener_ip_rural(aldea)
        personal_urbano_act_d = self.repo_trancicion_ip.obtener_ip_urbano_activos(
            aldea, self.anio)
        personal_rural_act_d = self.repo_trancicion_ip.obtener_ip_rural_activos(
            aldea, self.anio)

        personal_urbano = self.repo_trancicion_ip.obtener_ip_urbano_ot(
            aldea, cta_ip)
        personal_rural = self.repo_trancicion_ip.obtener_ip_rural_ot(
            aldea, cta_ip)
        personal_urbano_act = self.repo_trancicion_ip.obtener_ip_urbano_activos_ot(
            aldea, cta_ip, self.anio)
        personal_rural_act = self.repo_trancicion_ip.obtener_ip_rural_activos_ot(
            aldea, cta_ip, self.anio)

        personal_urbano['Total'] = personal_urbano['Total'] + \
            personal_urbano_d['Total']
        personal_rural['Total'] = personal_rural['Total'] + \
            personal_rural_d['Total']
        personal_urbano_act['Total'] = personal_urbano_act['Total'] + \
            personal_urbano_act_d['Total']
        personal_rural_act['Total'] = personal_rural_act['Total'] + \
            personal_rural_act_d['Total']

        data.append({
            'Tipo': 'Personal',
            'Valor_ins_urb': personal_urbano['Total'] or 0,
            'Valor_ins_rur': personal_rural['Total'] or 0,
            'Valor_act_urb': personal_urbano_act['Total'] or 0,
            'Valor_act_rur': personal_rural_act['Total'] or 0,
        })

        establecimiento_urbano = self.repo_trancicion_ics.obtener_ics_urbano(
            aldea)
        establecimiento_rural = self.repo_trancicion_ics.obtener_ics_rural(
            aldea)
        establecimiento_urbano_act = self.repo_trancicion_ics.obtener_ics_urbano_activos(
            aldea, self.anio)
        establecimiento_rural_act = self.repo_trancicion_ics.obtener_isc_rural_activos(
            aldea, self.anio)

        data.append({
            'Tipo': 'Industria, Comercio y Servicio',
            'Valor_ins_urb': establecimiento_urbano['Total'] or 0,
            'Valor_ins_rur': establecimiento_rural['Total'] or 0,
            'Valor_act_urb': establecimiento_urbano_act['Total'] or 0,
            'Valor_act_rur': establecimiento_rural_act['Total'] or 0,
        })

        if self.sys['TpoCuenta'] == 0:
            cta_ambiental = '111116'
            cta_selectivo = '111117'
        else:
            cta_ambiental = '1174'
            cta_selectivo = '1176'
        contri_ambien_urbano = self.repo_trancicion_amb.obtener_amb_urbano(
            aldea, cta_ambiental)
        contri_ambien_rural = self.repo_trancicion_amb.obtener_amb_rural(
            aldea, cta_ambiental)
        contri_ambien_urbano_act = self.repo_trancicion_amb.obtener_amb_urbano_activos(
            aldea, self.anio, cta_ambiental)
        contri_ambien_rural_act = self.repo_trancicion_amb.obtener_amb_rural_activos(
            aldea, self.anio, cta_ambiental)

        data.append({
            'Tipo': 'Extraccion, Explotacion de Recursos Naturales',
            'Valor_ins_urb': contri_ambien_urbano['Total'] or 0,
            'Valor_ins_rur': contri_ambien_rural['Total'] or 0,
            'Valor_act_urb': contri_ambien_urbano_act['Total'] or 0,
            'Valor_act_rur': contri_ambien_rural_act['Total'] or 0,
        })

        contri_ambien_urbano = self.repo_trancicion_amb.obtener_amb_urbano(
            aldea, cta_selectivo)
        contri_ambien_rural = self.repo_trancicion_amb.obtener_amb_rural(
            aldea, cta_selectivo)
        contri_ambien_urbano_act = self.repo_trancicion_amb.obtener_amb_urbano_activos(
            aldea, self.anio, cta_selectivo)
        contri_ambien_rural_act = self.repo_trancicion_amb.obtener_amb_rural_activos(
            aldea, self.anio, cta_selectivo)

        data.append({
            'Tipo': 'Selectivo A los Servicos de Telecomunicaciones',
            'Valor_ins_urb': contri_ambien_urbano['Total'] or 0,
            'Valor_ins_rur': contri_ambien_rural['Total'] or 0,
            'Valor_act_urb': contri_ambien_urbano_act['Total'] or 0,
            'Valor_act_rur': contri_ambien_rural_act['Total'] or 0,
        })

        cat_tec_urbano = self.repo_trancicion_bi.obtener_tec_anio_inicio(
            0, self.anio-3)
        cat_tec_rural = self.repo_trancicion_bi.obtener_tec_anio_inicio(
            1, self.anio-3)
        cat_tec_urbano_act = self.repo_trancicion_bi.obtener_tec_anio_fin(
            0)
        cat_tec_rural_act = self.repo_trancicion_bi.obtener_tec_anio_fin(
            1)

        data_catastro.append({
            'Tipo': 'Levantado (tecnificado)',
            'Valor_ins_urb': cat_tec_urbano['Total'] or 0,
            'Valor_ins_rur': cat_tec_urbano_act['Total'] or 0,
            'Valor_act_urb': cat_tec_rural['Total'] or 0,
            'Valor_act_rur': cat_tec_rural_act['Total'] or 0,
        })

        cat_tec_urbano = self.repo_trancicion_bi.obtener_dec_anio_inicio(
            0, self.anio-3)
        cat_tec_rural = self.repo_trancicion_bi.obtener_dec_anio_inicio(
            1, self.anio-3)
        cat_tec_urbano_act = self.repo_trancicion_bi.obtener_dec_anio_fin(
            0)
        cat_tec_rural_act = self.repo_trancicion_bi.obtener_dec_anio_fin(
            1)

        data_catastro.append({
            'Tipo': 'Levantado  (Multifinalitario)',
            'Valor_ins_urb': 'N/A',
            'Valor_ins_rur': 'N/A',
            'Valor_act_urb': 'N/A',
            'Valor_act_rur': 'N/A',
        })

        data_catastro.append({
            'Tipo': 'Simple (por declaración)',
            'Valor_ins_urb': cat_tec_urbano['Total'] or 0,
            'Valor_ins_rur': cat_tec_urbano_act['Total'] or 0,
            'Valor_act_urb': cat_tec_rural['Total'] or 0,
            'Valor_act_rur': cat_tec_rural_act['Total'] or 0,
        })
        data_sp = []
        dic_inicio = []
        dic_final = []
        if self.sys['TpoCuenta'] == 0:
            cta_sp = {
                "11111801": "Servicio de Agua Potable",
                "11111802": "Servicio de Alcantarillado Sanitario",
                "11111803": "Servicio de Alumbrado Público",
                "11111804": "Servicio de Tren de Aseo",
                "11111805": "Servicio de Conexiones, Reconexiones de Agua y Alcantarillado",
                "11111806": "Servicio de Bomberos",
                "11111807": "Servicio de Rastro Público",
                "11111808": "Servicio de Transporte de Carne",
                "11111809": "Servicio de Balanza Municipal",
                "11111810": "Servicio de Limpieza de Solares Baldíos",
                "11111811": "Servicio de Aseo, Mantenimiento de ¨Parques, Calles y Avenidas",
                "11111812": "Servicio de Limpieza de Cementerio",
                "11111813": "Servicio Secretariales Municipales",
                "11111814": "Servicio de muellaje",
                "11111815": "Servicio de Turismo",
                "11111816": "Servicio de Ciudadana",
                "11111817": "Servicio No Clasificado cta: 118-17",
                "11111818": "Servicio No Clasificado cta: 118-18",
                "11111819": "Servicio No Clasificado cta: 118-19",
                "11111820": "Tasa Ambiental",
                "11111899": "Otros servicios municipales"
            }

            dic_inicio = self.repo_trancicion_sp.obtener_sp_gob_inicio(
                cta_sp='111118', anio=self.anio-3)
            dic_final = self.repo_trancicion_sp.obtener_sp_gob_final(
                cta_sp='111118',)

        else:
            cta_sp = {"152190201": "Servicio de Agua Potable",
                      "152190202": "Servicio de Alcantarillado Sanitario",
                      "152190203": "Servicio de Alumbrado Público",
                      "152190204": "Servicio de Energía Eléctrica",
                      "152190205": "Servicio de Tren de Aseo",
                      "152190206": "Servicio de Bomberos",
                      "152190207": "Servicio de Agua por Riego",
                      "152190208": "Servicio de Purificadoras de Agua Municipales",
                      "125990102": "Tasa Balanza Municipal",
                      "125990108": "Servicio de Aseo, mantenimiento de parques, calles y avenidas",
                      "125990109": "Servicio de Aseo de cementerio",
                      "125990105": "Tasa Ambiental (protección y mejoramiento del ambiente)",
                      "125990119": "Tasa por Servicios Turísticos",
                      "125990103": "Tasa Seguridad ciudadana",
                      "125990104": "Tasa Vial",
                      "125990101": "Tasa Rastro público",
                      "125990213": "Limpieza de cementerios",
                      "125990211": "Servicios de muellaje",
                      "125990212": "Servicio de Limpieza de solares baldíos",
                      "152190101": "Servicios de Documentación",
                      "176301010": "Alquiler de Mercado", }

            sp_inicio = self.repo_trancicion_sp.obtener_sp_sami_inicio(
                cta_sp='1521902', anio=self.anio-3)
            dic_inicio = sp_inicio

            sp_inicio = self.repo_trancicion_sp.obtener_sp_sami_inicio(
                cta_sp='1259901', anio=self.anio-3)
            if sp_inicio:
                dic_inicio.extend(sp_inicio)

            sp_inicio = self.repo_trancicion_sp.obtener_sp_sami_inicio(
                cta_sp='1259902', anio=self.anio-3)
            if sp_inicio:
                dic_inicio.extend(sp_inicio)

            sp_inicio = self.repo_trancicion_sp.obtener_sp_sami_inicio(
                cta_sp='1521901', anio=self.anio-3)
            if sp_inicio:
                dic_inicio.extend(sp_inicio)

            sp_inicio = self.repo_trancicion_sp.obtener_sp_sami_inicio(
                cta_sp='1763010', anio=self.anio-3)
            if sp_inicio:
                dic_inicio.extend(sp_inicio)

            sp_final = self.repo_trancicion_sp.obtener_sp_sami_final(
                cta_sp='1521902')
            dic_final = sp_final
            sp_final = self.repo_trancicion_sp.obtener_sp_sami_final(
                cta_sp='1259901')
            if sp_final:
                dic_final.extend(sp_final)
            sp_final = self.repo_trancicion_sp.obtener_sp_sami_final(
                cta_sp='1259902')
            if sp_final:
                dic_final.extend(sp_final)
            sp_final = self.repo_trancicion_sp.obtener_sp_sami_final(
                cta_sp='1521901')
            if sp_final:
                dic_final.extend(sp_final)
            sp_final = self.repo_trancicion_sp.obtener_sp_sami_final(
                cta_sp='1763010')
            if sp_final:
                dic_final.extend(sp_final)

        df_inicio = pd.DataFrame(dic_inicio)

        df_final = pd.DataFrame(dic_final)

        df = df_inicio.merge(df_final, on="Cuenta", how="right")
        df = df.fillna(0)

        for _, data_s in df.iterrows():
            cuenta = data_s['Cuenta']
            tipo = cta_sp.get(cuenta, "Servicio desconocido")
            if tipo == "Servicio desconocido":
                continue
            val_inicio = int(data_s.get('Total_x', data_s.get('Total_x', 0)))
            val_final = data_s.get('Total_y', 0)

            data_sp.append({
                'Cuenta': cuenta,
                'Tipo': tipo,
                'Valor_inicio': val_inicio,
                'Valor_final': val_final
            })

        if not data:
            raise ValueError(
                "No se encontraron datos de Trancicion y Traspaso.")
        return data, data_catastro, data_sp
