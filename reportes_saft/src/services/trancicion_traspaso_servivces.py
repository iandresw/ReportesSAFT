from datetime import datetime
from repositories.trancicion_ip_repository import TrancicionIPRepository
from repositories.trancicion_bi_repository import TrancicionBIRepository
from services.parametro_service import ParametroService


class TrancicionTraspasoService:
    def __init__(self, conexion, sistem):
        self.repo_trancicion_ip = TrancicionIPRepository(conexion)
        self.repo_trancicion_bi = TrancicionBIRepository(conexion)
        self.parametro_systema = ParametroService(conexion)
        self.sys = sistem
        self.data = []
        self.anio = datetime.now().year

    def obtener_contribuyentes(self):
        data = []
        propiedades_urbano = self.repo_trancicion_bi.obtener_bi_urbano()
        propiedades_rural = self.repo_trancicion_bi.obtener_bi_rural()
        propiedades_urbano_act = self.repo_trancicion_bi.obtener_bi_urbano_activos(
            self.anio)
        propiedades_rural_act = self.repo_trancicion_bi.obtener_bi_rural_activos(
            self.anio)

        data.append({
            'Tipo': 'BIENES INMUEBLES',
            'Valor_ins_urb': propiedades_urbano['Total'] or 0,
            'Valor_ins_rur': propiedades_rural['Total'] or 0,
            'Valor_act_urb': propiedades_urbano_act['Total'] or 0,
            'Valor_act_rur': propiedades_rural_act['Total'] or 0,
        })

        cta_ip = self.sys['CtaIngresoIP']
        personal_urbano = self.repo_trancicion_ip.obtener_ip_urbano("141301")
        personal_rural = self.repo_trancicion_ip.obtener_ip_rural("141301")
        personal_urbano_act = self.repo_trancicion_ip.obtener_ip_urbano_activos(
            "141301", self.anio)
        personal_rural_act = self.repo_trancicion_ip.obtener_ip_rural_activos(
            "141301", self.anio)

        data.append({
            'Tipo': 'IMPUESTO PERSONAL DECLARADO',
            'Valor_ins_urb': personal_urbano['Total'] or 0,
            'Valor_ins_rur': personal_rural['Total'] or 0,
            'Valor_act_urb': personal_urbano_act['Total'] or 0,
            'Valor_act_rur': personal_rural_act['Total'] or 0,
        })

        personal_urbano = self.repo_trancicion_ip.obtener_ip_urbano_ot(
            "141301", cta_ip)
        personal_rural = self.repo_trancicion_ip.obtener_ip_rural_ot(
            "141301", cta_ip)
        personal_urbano_act = self.repo_trancicion_ip.obtener_ip_urbano_activos_ot(
            "141301", cta_ip, self.anio)
        personal_rural_act = self.repo_trancicion_ip.obtener_ip_rural_activos_ot(
            "141301", cta_ip, self.anio)

        data.append({
            'Tipo': 'IMPUESTO PERSONAL OTRAS TASAS',
            'Valor_ins_urb': personal_urbano['Total'] or 0,
            'Valor_ins_rur': personal_rural['Total'] or 0,
            'Valor_act_urb': personal_urbano_act['Total'] or 0,
            'Valor_act_rur': personal_rural_act['Total'] or 0,
        })

        if not self.data:
            raise ValueError("No se encontraron datos de mora BI.")
        return self.data
