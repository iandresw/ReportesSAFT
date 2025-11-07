from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


class MoraSPReport:
    def __init__(self, datos_agua, datos_alcantarillado, datos_tren, datos_bombero, datos_solares, datos_parques, datos_lim_cementerio, datos_ase_cementerio, datos_ambiente, municipio, titulo_reporte):
        self.datos_A = datos_agua
        self.datos_B = datos_alcantarillado
        self.datos_C = datos_tren
        self.datos_D = datos_bombero
        self.datos_E = datos_solares
        self.datos_F = datos_parques
        self.datos_G = datos_lim_cementerio
        self.datos_H = datos_ase_cementerio
        self.datos_I = datos_ambiente

        self.municipio = municipio
        self.titulo = titulo_reporte

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter)
        elementos = []
        estilos = getSampleStyleSheet()

        # Encabezado del reporte
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
        # DATOS TABLA DE SERVICIO DE AGUA
        if self.datos_A:
            subtitulo_A = Paragraph(
                f"<b>Mora Servicio de Agua</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_A)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_A:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_A = Table(filas, colWidths=[90, 300, 100])
            tabla_A.setStyle(stylo_table)
            elementos.append(tabla_A)

        # DATOS TABLA DE SERVICIO DE Alcantarillado
        if self.datos_B:
            subtitulo_A = Paragraph(
                f"<b>Mora Servicio de Alcantarillado</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_A)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_B:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_B = Table(filas, colWidths=[90, 300, 100])
            tabla_B.setStyle(stylo_table)
            elementos.append(tabla_B)

        # DATOS TABLA DE SERVICIO DE TREN DE ASEO
        if self.datos_C:
            subtitulo_C = Paragraph(
                f"<b>Mora Servicio de Tren de Aseo</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_C)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_C:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_C = Table(filas, colWidths=[90, 300, 100])
            tabla_C.setStyle(stylo_table)
            elementos.append(tabla_C)

        # DATOS TABLA DE SERVICIO DE BOMBEROS
        if self.datos_D:
            subtitulo_D = Paragraph(
                f"<b>Mora Servicio de Bombero</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_D)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_D:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_D = Table(filas, colWidths=[90, 300, 100])
            tabla_D.setStyle(stylo_table)
            elementos.append(tabla_D)

        # DATOS TABLA DE SERVICIO DE LIMPIEZA SOLAR BALDIO
        if self.datos_E:
            subtitulo_E = Paragraph(
                f"<b>Mora Servicio de Limpieza de Solares Baldios</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_E)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_E:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_E = Table(filas, colWidths=[90, 300, 100])
            tabla_E.setStyle(stylo_table)
            elementos.append(tabla_E)

        # DATOS TABLA DE SERVICIO DE MANTENIMIENTO DE PARQUE Y AVENIDAS
        if self.datos_F:
            subtitulo_F = Paragraph(
                f"<b>Mora Servicio Mantenimiento de Parques, Calles Y Avenidas</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_F)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_F:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_F = Table(filas, colWidths=[90, 300, 100])
            tabla_F.setStyle(stylo_table)
            elementos.append(tabla_F)

        # DATOS TABLA DE SERVICIO DE LIMPIEZA DE CEMENTERIO
        if self.datos_G:
            subtitulo_G = Paragraph(
                f"<b>Mora Servicio Limpieza de Cementerio</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_G)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_G:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_G = Table(filas, colWidths=[90, 300, 100])
            tabla_G.setStyle(stylo_table)
            elementos.append(tabla_G)

        # DATOS TABLA DE SERVICIO DE ASEO DE CEMENTERIO
        if self.datos_H:
            subtitulo_H = Paragraph(
                f"<b>Mora Servicio Limpieza de Cementerio</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_H)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_H:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])

            tabla_H = Table(filas, colWidths=[90, 300, 100])
            tabla_H.setStyle(stylo_table)
            elementos.append(tabla_H)

        # DATOS TABLA DE TASA AMBIENTAL
        if self.datos_I:
            subtitulo_I = Paragraph(
                f"<b>Mora Tasa Ambiental</b>",
                estilos["Normal"],
            )
            elementos.append(Spacer(1, 12))
            elementos.append(subtitulo_I)
            elementos.append(Spacer(1, 24))

            encabezados = ["Cuenta", "Descripcion", "Monto (L)"]
            filas = [encabezados]

            sub_total = 0
            for item in self.datos_I:
                monto = (item["Valor"]) if item["Valor"] else 0
                filas.append([item["Cuenta"], item["Tipo"], f"{monto:,.2f}"])
                total += monto
                sub_total += monto
            filas.append(["", "SUB-TOTAL", f"{sub_total:,.2f}"])
            filas.append(["", "TOTAL", f"{total:,.2f}"])
            tabla_I = Table(filas, colWidths=[90, 300, 100])
            tabla_I.setStyle(stylo_table)
            elementos.append(tabla_I)

        elementos.append(Spacer(1, 20))

        footer = Paragraph(
            "<b>Generado por el sistema SAFT</b>",
            estilos["Normal"],
        )
        elementos.append(footer)

        doc.build(elementos)
