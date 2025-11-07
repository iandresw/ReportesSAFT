from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


class MoraBIReport:
    def __init__(self, datos, municipio, titulo_reporte):
        self.datos = datos
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

        elementos.append(titulo)
        elementos.append(Spacer(1, 12))
        elementos.append(fecha)
        elementos.append(Spacer(1, 24))

        # 🧮 Tabla con los datos
        encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
        filas = [encabezados]

        total = 0
        for item in self.datos:
            monto = (item["Valor"]) if item["Valor"] else 0
            filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
            total += monto

        filas.append(["", "TOTAL", f"{total:,.2f}"])

        tabla = Table(filas, colWidths=[90, 300, 100])
        tabla.setStyle(
            TableStyle(
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
        )

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        footer = Paragraph(
            "<b>Generado por el sistema SAFT</b>",
            estilos["Normal"],
        )
        elementos.append(footer)

        doc.build(elementos)
