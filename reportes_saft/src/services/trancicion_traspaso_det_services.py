from datetime import datetime
from repositories.trancicion_ip_repository import TrancicionIPRepository
from repositories.trancicion_bi_repository import TrancicionBIRepository
from repositories.trancicion_ics_repository import TrancicionICSRepository
from repositories.trancicion_amb_reposiory import TrancicionAMBRepository
from repositories.trancicion_ps_reposiory import TrancicionSPRepository

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from datetime import datetime
from repositories.aldea_repository import AldeaRepository
from services.parametro_service import ParametroService
from reports.trancicion_det_ics_report import TrancicionICSDetalleReport


class TrancicionTraspasoDetalleService:
    def __init__(self, conexion, sistem):
        self.repo_trancicion_ip = TrancicionIPRepository(conexion)
        self.repo_trancicion_bi = TrancicionBIRepository(conexion)
        self.repo_trancicion_ics = TrancicionICSRepository(conexion)
        self.repo_trancicion_ot = TrancicionAMBRepository(conexion)
        self.repo_trancicion_sp = TrancicionSPRepository(conexion)
        self.repo_aldea = AldeaRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem
        self.rpt_excel_ics = TrancicionICSDetalleReport(self.sys)
        self.codAldea = self.repo_aldea.obtener_aldea_urbana()
        self.anio = datetime.now().year
        self.anio_inicio = 2022

    def obtener_contribuyentes_ip(self, ruta_excel: str):
        aldea = self.codAldea['CodAldea']
        cta_ip = self.sys['CtaIngresoIP']
        contribuyente_urbano = self.repo_trancicion_ip.obtener_ip_urbano_detalle(
            codAldea=aldea)
        contribuyente_rural = self.repo_trancicion_ip.obtener_ip_rural_detalle(
            codAldea=aldea)
        contribuyente_urbano_act = self.repo_trancicion_ip.obtener_ip_urbano_activos_detalle(
            codAldea=aldea, anio=self.anio)
        contribuyente_rurales_act = self.repo_trancicion_ip.obtener_ip_rural_activos_detalle(
            codAldea=aldea, anio=self.anio)

        contribuyente_urbano_ot = self.repo_trancicion_ip.obtener_ip_urbano_ot_detalle(
            CodAldea=aldea, cta_ip=cta_ip)
        contribuyente_rural_ot = self.repo_trancicion_ip.obtener_ip_rural_ot_detalle(
            CodAldea=aldea, cta_ip=cta_ip)
        contribuyente_urbano_act_ot = self.repo_trancicion_ip.obtener_ip_urbano_activos_ot_detalle(
            codAldea=aldea, cta_ip=cta_ip, anio=self.anio)
        contribuyente_rurales_act_ot = self.repo_trancicion_ip.obtener_ip_rural_activos_ot_detalle(
            codAldea=aldea, cta_ip=cta_ip, anio=self.anio)
        if contribuyente_urbano_ot:   # True si la lista tiene elementos
            contribuyente_urbano.extend(contribuyente_urbano_ot)
        if contribuyente_rural_ot:
            contribuyente_rural.extend(contribuyente_rural_ot)
        if contribuyente_urbano_act_ot:
            contribuyente_urbano_act.extend(contribuyente_urbano_act_ot)
        if contribuyente_rurales_act_ot:
            contribuyente_rurales_act.extend(contribuyente_rurales_act_ot)
        ruta_excel = self.rpt_excel_ics.generar_excel(
            contribuyente_urbano, contribuyente_rural, contribuyente_urbano_act, contribuyente_rurales_act, ruta_excel, "IP")

        return ruta_excel

    def obtener_contribuyentes_bi(self, ruta_excel: str):

        bi_urbano = self.repo_trancicion_bi.obtener_bi_urbano_detalle()
        bi_rural = self.repo_trancicion_bi.obtener_bi_rural_detalle()
        bi_urbano_act = self.repo_trancicion_bi.obtener_bi_urbano_activos_detalle(
            anio=self.anio)
        bi_rurales_act = self.repo_trancicion_bi.obtener_bi_rural_activos_detalle(
            anio=self.anio)

        bi_tec_urbano_inicio = self.repo_trancicion_bi.obtener_tec_anio_inicio_detalle(
            0, self.anio-3)
        bi_tec_rural_inicio = self.repo_trancicion_bi.obtener_tec_anio_inicio_detalle(
            1, self.anio-3)
        bi_tec_urbano_final = self.repo_trancicion_bi.obtener_tec_anio_fin_detalle(
            0)
        bi_tec_rurales_final = self.repo_trancicion_bi.obtener_tec_anio_fin_detalle(
            1)

        bi_dec_rural_inicio = self.repo_trancicion_bi.obtener_dec_anio_inicio_detalle(
            1, self.anio-3)
        bi_dec_urbano_inicio = self.repo_trancicion_bi.obtener_dec_anio_inicio_detalle(
            0, self.anio-3)
        bi_dec_urbano_final = self.repo_trancicion_bi.obtener_dec_anio_fin_detalle(
            0)
        bi_dec_rurales_final = self.repo_trancicion_bi.obtener_dec_anio_fin_detalle(
            1)

        with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
            pd.DataFrame(bi_urbano).to_excel(
                writer, sheet_name="BI Urbano", index=False)
            pd.DataFrame(bi_rural).to_excel(
                writer, sheet_name="BI Rural", index=False)
            pd.DataFrame(bi_urbano_act).to_excel(
                writer, sheet_name="BI Urbano Activos", index=False)
            pd.DataFrame(bi_rurales_act).to_excel(
                writer, sheet_name="BI Rural Activos", index=False)

            pd.DataFrame(bi_tec_urbano_inicio).to_excel(
                writer, sheet_name="BI Urbano Inicio Tec.", index=False)
            pd.DataFrame(bi_tec_rural_inicio).to_excel(
                writer, sheet_name="BI Rural Inicio Tec.", index=False)
            pd.DataFrame(bi_tec_urbano_final).to_excel(
                writer, sheet_name="BI Urbano Final Tec", index=False)
            pd.DataFrame(bi_tec_rurales_final).to_excel(
                writer, sheet_name="BI Rural Final Tec", index=False)

            pd.DataFrame(bi_dec_rural_inicio).to_excel(
                writer, sheet_name="BI  Urbano Inicio Declarado.", index=False)
            pd.DataFrame(bi_dec_urbano_inicio).to_excel(
                writer, sheet_name="BI  Rural Inicio Declarado.", index=False)
            pd.DataFrame(bi_dec_urbano_final).to_excel(
                writer, sheet_name="BI Urbano Final Declarado", index=False)
            pd.DataFrame(bi_dec_rurales_final).to_excel(
                writer, sheet_name="BI Rural Final Declarado", index=False)

        return ruta_excel

    def obtener_contribuyentes_ics(self, ruta_excel: str):
        aldea = self.codAldea['CodAldea']
        ics_urbano = self.repo_trancicion_ics.obtener_ics_urbano_detalle(aldea)
        ics_rural = self.repo_trancicion_ics.obtener_ics_rural_detalle(aldea)
        ics_urbano_act = self.repo_trancicion_ics.obtener_isc_urbano_activos_detalle(
            codAldea=aldea, anio=self.anio)
        ics_rurales_act = self.repo_trancicion_ics.obtener_isc_rural_activos_detalle(
            codAldea=aldea, anio=self.anio)
        ruta_excel = self.rpt_excel_ics.generar_excel(
            ics_urbano, ics_rural, ics_urbano_act, ics_rurales_act, ruta_excel, "ICS")
        return ruta_excel

    def obtener_contribuyentes_amb(self, ruta_excel: str):
        aldea = self.codAldea['CodAldea']
        if self.sys['TpoCuenta'] == 0:
            cta_ambiental = '111116'
        else:
            cta_ambiental = '1174'
        amb_urbano = self.repo_trancicion_ot.obtener_amb_urbano_detalle(
            aldea, ctaIngreso=cta_ambiental)
        amb_rural = self.repo_trancicion_ot.obtener_amb_rural_detalle(
            aldea, ctaIngreso=cta_ambiental)
        amb_urbano_act = self.repo_trancicion_ot.obtener_amb_urbano_activos_detalle(
            codAldea=aldea, anio=self.anio, ctaIngreso=cta_ambiental)
        amb_rurales_act = self.repo_trancicion_ot.obtener_amb_rural_activos_detalle(
            codAldea=aldea, anio=self.anio, ctaIngreso=cta_ambiental)
        ruta_excel = self.rpt_excel_ics.generar_excel(
            amb_urbano, amb_rural, amb_urbano_act, amb_rurales_act, ruta_excel, "IER")
        return ruta_excel

    def obtener_contribuyentes_ist(self, ruta_excel: str):
        aldea = self.codAldea['CodAldea']
        if self.sys['TpoCuenta'] == 0:
            cta_selectivo = '111117'
        else:
            cta_selectivo = '1176'
        amb_urbano = self.repo_trancicion_ot.obtener_amb_urbano_detalle(
            aldea, ctaIngreso=cta_selectivo)
        amb_rural = self.repo_trancicion_ot.obtener_amb_rural_detalle(
            aldea, ctaIngreso=cta_selectivo)
        amb_urbano_act = self.repo_trancicion_ot.obtener_amb_urbano_activos_detalle(
            codAldea=aldea, anio=self.anio, ctaIngreso=cta_selectivo)
        amb_rurales_act = self.repo_trancicion_ot.obtener_amb_rural_activos_detalle(
            codAldea=aldea, anio=self.anio, ctaIngreso=cta_selectivo)
        ruta_excel = self.rpt_excel_ics.generar_excel(
            amb_urbano, amb_rural, amb_urbano_act, amb_rurales_act, ruta_excel, "IER")
        return ruta_excel

    def obtener_contribuyentes_sp(self, ruta_excel: str):
        resultados = {}
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
                "11111811": "Servicio de Aseo, Mantenimiento de Parques, Calles y Avenidas",
                "11111812": "Servicio de Limpieza de Cementerio",
                "11111813": "Servicio Secretariales Municipales",
                "11111814": "Servicio de muellaje",
                "11111815": "Servicio de Turismo",
                "11111816": "Servicio de Ciudadana",
                "11111817": "Servicio No Clasificado cta 118-17",
                "11111818": "Servicio No Clasificado cta 118-18",
                "11111819": "Servicio No Clasificado cta 118-19",
                "11111820": "Tasa Ambiental",
                "11111899": "Otros servicios municipales"
            }
            for cta, nombre in cta_sp.items():
                servicio_inicio = self.repo_trancicion_sp.obtener_sp_gob_inicio_detalle(
                    cta_sp=cta, anio=self.anio_inicio)
                servicio_final = self.repo_trancicion_sp.obtener_sp_gob_final_detalle(
                    cta_sp=cta)
                resultados[nombre] = {
                    "inicio": servicio_inicio,
                    "final": servicio_final
                }
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
                      "125990212": "Servicio de Limpieza de solares baldíos",
                      "125990108": "Servicio de Aseo, mantenimiento de parques, calles y avenidas",
                      "125990109": "Servicio de Aseo de cementerio",
                      "152190101": "Servicios de Documentación",
                      "125990211": "Servicios de muellaje",
                      "125990105": "Tasa Ambiental (protección y mejoramiento del ambiente)",
                      "125990119": "Tasa por Servicios Turísticos",
                      "125990103": "Tasa Seguridad ciudadana",
                      "125990104": "Tasa Vial",
                      "125990101": "Tasa Rastro público",
                      "125990213": "Limpieza de cementerios", }
            for cta, nombre in cta_sp.items():
                servicio_inicio = self.repo_trancicion_sp.obtener_sp_sami_inicio_detalle(
                    cta_sp=cta, anio=self.anio_inicio)
                servicio_final = self.repo_trancicion_sp.obtener_sp_sami_final_detalle(
                    cta_sp=cta)
                resultados[nombre] = {
                    "inicio": servicio_inicio,
                    "final": servicio_final
                }

        with pd.ExcelWriter(ruta_excel, engine="openpyxl") as writer:
            for nombre_servicio, datos in resultados.items():
                hoja_inicio = f"{nombre_servicio} inicio"
                hoja_final = f"{nombre_servicio} final"
                if datos["inicio"]:
                    pd.DataFrame(datos["inicio"]).to_excel(
                        writer, sheet_name=hoja_inicio[:30], index=False)
                if datos["final"]:
                    pd.DataFrame(datos["final"]).to_excel(
                        writer, sheet_name=hoja_final[:30], index=False)

        return ruta_excel
