from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from ui.ui_style_table import table_style, columa_style
from datetime import datetime


class TrancicionReport:
    def __init__(self, datos, datos_catastro,  data_sp, municipio, titulo_reporte):
        self.datos = datos
        self.datos_cat = datos_catastro
        self.datos_sp = data_sp
        self.municipio = municipio
        self.titulo = titulo_reporte

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter)
        elementos = []
        estilos = getSampleStyleSheet()

        titulo = Paragraph(
            f"<b>REPORTE DE {self.titulo} </b><br/>{self.municipio['NombreMuni']} - {self.municipio['NombreDepto']}",
            estilos["Title"],
        )
        fecha = Paragraph(
            f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos["Normal"],
        )

        elementos.append(titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)
        elementos.append(Spacer(1, 24))
        estilo_encabezado = columa_style()
        estilo_tabla = table_style()
        encabezados = [
            Paragraph("Detalle", estilo_encabezado),
            Paragraph("Urbanos Inscritos", estilo_encabezado),
            Paragraph("Rurales Inscritos", estilo_encabezado),
            Paragraph("Urbanos Activos", estilo_encabezado),
            Paragraph("Rurales Activos", estilo_encabezado)
        ]
        filas = [encabezados]
        for item in self.datos:
            ins_urb = (item["Valor_ins_urb"]) if item["Valor_ins_urb"] else 0
            ins_rur = (item["Valor_ins_rur"]) if item["Valor_ins_rur"] else 0
            act_urb = (item["Valor_act_urb"]) if item["Valor_act_urb"] else 0
            act_rur = (item["Valor_act_rur"]) if item["Valor_act_rur"] else 0
            filas.append(
                [item["Tipo"], f"{ins_urb}", f"{ins_rur}", f"{act_urb}", f"{act_rur}"])
        tabla = Table(filas, colWidths=[240, 80, 80, 80, 80])
        tabla.setStyle(estilo_tabla)
        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        titulo_catastro = Paragraph(
            f"<b>Catastro Tecnificado - Declarado:</b>",
            estilos["Normal"],
        )
        elementos.append(Spacer(1, 12))
        elementos.append(titulo_catastro)
        elementos.append(Spacer(1, 24))
        encabezados_cat = [
            Paragraph("Condición de Implementación", estilo_encabezado),
            Paragraph("Año de Inicio de Gobierno Municipal Urbano",
                      estilo_encabezado),
            Paragraph("Año de Final de Gobierno Municipal Urbano",
                      estilo_encabezado),
            Paragraph("Año de Inicio de Gobierno Municipal Rural",
                      estilo_encabezado),
            Paragraph("Año de Final de Gobierno Municipal Rural",
                      estilo_encabezado)
        ]
        filas = [encabezados_cat]
        for item in self.datos_cat:
            ins_urb = (item["Valor_ins_urb"]) if item["Valor_ins_urb"] else 0
            ins_rur = (item["Valor_ins_rur"]) if item["Valor_ins_rur"] else 0
            act_urb = (item["Valor_act_urb"]) if item["Valor_act_urb"] else 0
            act_rur = (item["Valor_act_rur"]) if item["Valor_act_rur"] else 0
            # type: ignore
            filas.append(
                [item["Tipo"], f"{ins_urb}", f"{ins_rur}", f"{act_urb}", f"{act_rur}"])
        tabla_cat = Table(filas, colWidths=[240, 80, 80, 80, 80])
        tabla_cat.setStyle(estilo_tabla)
        elementos.append(tabla_cat)
        elementos.append(Spacer(1, 20))

        titulo_sp = Paragraph(
            f"<b>Servicios Publicos Municipales:</b>",
            estilos["Normal"],
        )
        elementos.append(Spacer(1, 12))
        elementos.append(titulo_sp)
        elementos.append(Spacer(1, 24))
        encabezados_sp = [
            Paragraph("Cuenta", estilo_encabezado),
            Paragraph("Tipos de Servicios",
                      estilo_encabezado),
            Paragraph("Año de Inicio de Gobierno Municipal",
                      estilo_encabezado),
            Paragraph("Año de Final de Gobierno Municipal", estilo_encabezado)
        ]
        filas = [encabezados_sp]
        for item in self.datos_sp:
            num_ab_inicio = (item["Valor_inicio"]
                             ) if item["Valor_inicio"] else 0
            num_ab_final = (item["Valor_final"]
                            ) if item["Valor_final"] else 0
            # type: ignore
            filas.append([item["Tipo"], item["Cuenta"],
                         f"{num_ab_inicio}", f"{num_ab_final}"])
        tabla_cat = Table(filas, colWidths=[320, 80, 80, 80])
        tabla_cat.setStyle(estilo_tabla)
        elementos.append(tabla_cat)
        elementos.append(Spacer(1, 20))

        footer = Paragraph(
            "<b>Generado por el sistema SAFT</b>",
            estilos["Normal"],
        )
        elementos.append(footer)

        doc.build(elementos)
