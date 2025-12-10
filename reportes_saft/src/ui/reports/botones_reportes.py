# ui/reportes/botones_reportes.py
from ui.ui_botones import create_boton


def botones_mora(vista):
    return [
        create_boton("Mora Bienes Inmuebles", vista.on_mora_bi),
        create_boton("Mora Impuesto Personal", vista.on_mora_ip),
        create_boton("Mora Industria Comercio y Servicio", vista.on_mora_ics),
        create_boton("Mora Servicios Públicos", vista.on_mora_sp),
        create_boton("Mora vs Ingresos Aldea General",
                     vista.abrir_modal_mora_vs_ingresos),
        create_boton("Mora vs Ingresos BI (Aldea - Año)",
                     vista.abrir_modal_mora_aldea_anio),
        create_boton("Analisis de Ingresos",
                     vista.abril_modal_analisi_ingresos),
    ]


def botones_otros(vista):
    return [
        create_boton("Transición y Traspaso", vista.rept_trancicicon),
        create_boton("Detalle IP", vista.rpt_trancicion_det_ip),
        create_boton("Detalle BI", vista.rpt_trancicion_det_bi),
        create_boton("Detalle ICS", vista.rpt_trancicion_det_ics),
        create_boton("Detalle AMB", vista.rpt_trancicion_det_amp),
        create_boton("Detalle IST", vista.rpt_trancicion_det_ist),
        create_boton("Detalle SP", vista.rpt_trancicion_det_sp),
        # create_boton("Anula Plan de Pago", vista.abril_modal_anula_pp),
    ]
