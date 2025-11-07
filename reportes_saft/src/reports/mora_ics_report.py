from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


class MoraICSReport:
    def __init__(self, datos_i, datos_c, datos_s, datos_t, municipio, titulo_reporte):
        self.datos_i = datos_i
        self.datos_c = datos_c
        self.datos_s = datos_s
        self.datos_t = datos_t
        self.municipio = municipio
        self.titulo = titulo_reporte

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter)
        elementos = []
        estilos = getSampleStyleSheet()

        # 🏛️ Encabezado del reporte
        titulo = Paragraph(
            f"<b>REPORTE DE MORA {self.titulo} </b><br/>{self.municipio['NombreMuni']} - {self.municipio['NombreDepto']}",
            estilos["Title"],
        )
        fecha = Paragraph(
            f"<b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos["Normal"],
        )
        stylo_table = TableStyle(
            [
                # Encabezado
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                # Bordes y fondo general
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("BACKGROUND", (-1, -1), (-1, -1), colors.lightgrey),

                # 🔹 Alineaciones personalizadas por columna
                # Primera columna centrada
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                # Segunda columna a la izquierda
                ("ALIGN", (1, 0), (1, -1), "LEFT"),
                # Tercera columna a la derecha
                ("ALIGN", (2, 0), (2, -1), "RIGHT"),
            ]
        )
        elementos.append(titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)
        elementos.append(Spacer(1, 24))
        total = 0
        # DATOS TABLA DE INDUSTRIA
        subtitulo_i = Paragraph(
            f"<b>Mora Impuesto de Industria</b>",
            estilos["Normal"],
        )
        elementos.append(Spacer(1, 12))
        elementos.append(subtitulo_i)
        elementos.append(Spacer(1, 24))

        encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
        filas = [encabezados]

        sub_total = 0
        for item in self.datos_i:
            monto = (item["Valor"]) if item["Valor"] else 0
            filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
            total += monto
            sub_total += monto
        filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

        tabla_i = Table(filas, colWidths=[90, 300, 100])
        tabla_i.setStyle(stylo_table)
        elementos.append(tabla_i)
        # DATOS TABLA DE COMERCIO
        subtitulo_c = Paragraph(
            f"<b>Mora Impuesto de Comercio</b>",
            estilos["Normal"],
        )
        elementos.append(Spacer(1, 12))
        elementos.append(subtitulo_c)
        elementos.append(Spacer(1, 24))

        encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
        filas = [encabezados]

        sub_total = 0
        for item in self.datos_c:
            monto = (item["Valor"]) if item["Valor"] else 0
            filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
            total += monto
            sub_total += monto
        filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])
        tabla_c = Table(filas, colWidths=[90, 300, 100])
        tabla_c.setStyle(stylo_table)
        elementos.append(tabla_c)
        # DATOS TABLA DE SERVICIO
        subtitulo_s = Paragraph(
            f"<b>Mora Impuesto de Servicio</b>",
            estilos["Normal"],
        )
        elementos.append(Spacer(1, 12))
        elementos.append(subtitulo_s)
        elementos.append(Spacer(1, 24))

        encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
        filas = [encabezados]

        sub_total = 0
        for item in self.datos_s:
            monto = (item["Valor"]) if item["Valor"] else 0
            filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
            total += monto
            sub_total += monto
        filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])
        tabla_s = Table(filas, colWidths=[90, 300, 100])
        tabla_s.setStyle(stylo_table)
        elementos.append(tabla_s)

        # DATOS TABLA DE TASAS
        subtitulo_t = Paragraph(
            f"<b>Derechos, Tasas, Multas</b>",
            estilos["Normal"],
        )
        elementos.append(Spacer(1, 12))
        elementos.append(subtitulo_t)
        elementos.append(Spacer(1, 24))

        encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
        filas = [encabezados]

        sub_total = 0
        for item in self.datos_t:
            monto = (item["Valor"]) if item["Valor"] else 0
            filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
            total += monto
            sub_total += monto
        filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])
        filas.append(["", "TOTAL", f"{total:,.2f}"])
        tabla_t = Table(filas, colWidths=[90, 300, 100])
        tabla_t.setStyle(stylo_table)
        elementos.append(tabla_t)

        elementos.append(Spacer(1, 20))

        footer = Paragraph(
            "<b>Generado por el sistema SAFT</b>",
            estilos["Normal"],
        )
        elementos.append(footer)

        doc.build(elementos)
