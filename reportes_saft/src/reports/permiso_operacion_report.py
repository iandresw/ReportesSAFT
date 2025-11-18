from reportlab.lib.pagesizes import letter
from reportlab.lib.fonts import addMapping
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from models.tra_permop import Tra_PermOpe
from ui.ui_style_table import table_per_ope, estilos_parrafo, table_per_ope_2
import os
import locale
import json
import qrcode
from io import BytesIO


locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
# ==== Registrar fuentes Malgun desde carpeta local ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sube un nivel desde reports/
FONTS_DIR = os.path.join(BASE_DIR, "..", "fonts")

# Rutas de fuentes
font_regular = os.path.join(FONTS_DIR, "malgun.ttf")
font_bold = os.path.join(FONTS_DIR, "malgunbd.ttf")
font_GOTHICB = os.path.join(FONTS_DIR, "GOTHICB.TTF")
font_GOTHICB0 = os.path.join(FONTS_DIR, "GOTHICB0.TTF")
font_Jhenghei = os.path.join(FONTS_DIR, "Jhenghei.ttf")
font_Century_Gothic = os.path.join(FONTS_DIR, "Century-Gothic.ttf")

# Registrar fuentes si existen
if os.path.exists(font_regular) and os.path.exists(font_bold):
    pdfmetrics.registerFont(TTFont('Malgun', font_regular))
    pdfmetrics.registerFont(TTFont('Malgun-Bold', font_bold))
    pdfmetrics.registerFont(TTFont('GOTHICB0', font_GOTHICB0))
    pdfmetrics.registerFont(TTFont('GOTHICB', font_GOTHICB))
    pdfmetrics.registerFont(TTFont('Jhenghei', font_Jhenghei))
    pdfmetrics.registerFont(TTFont('Century-Gothic', font_Jhenghei))
    addMapping('Malgun', 0, 0, 'Malgun')
    addMapping('Malgun', 1, 0, 'Malgun-Bold')
    addMapping('GOTHICB0', 0, 0, 'GOTHICB0')
    addMapping('GOTHICB', 1, 0, 'GOTHICB')
    addMapping('Jhenghei', 0, 0, 'Jhenghei')
    addMapping('Century-Gothic', 1, 0, 'Century-Gothic')
else:
    print("Advertencia: no se encontraron las fuentes Malgun en /fonts/")


class PermisoOperacionReport:
    def __init__(self, datos: Tra_PermOpe, municipio, titulo_reporte, firma_justicia=False):
        self.datos = datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.justicia_firma = firma_justicia

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter,
                                leftMargin=40,
                                rightMargin=40,
                                topMargin=20,
                                bottomMargin=20)
        elementos = []
        permiso_datos = json.dumps({
            "permiso": self.datos.NumRecibo,
            "nombre": self.datos.Negocio,
            "fecha": self.datos.Fecha.strftime("%d/%m/%Y"),
            "id": self.datos.Identidad,
            "Propietario": self.datos.Propietario,
            "Periodo": self.datos.Periodo
        }, ensure_ascii=False)

        estilos = estilos_parrafo()
        estilos_tabla = table_per_ope()
        estilos_tabla2 = table_per_ope_2()
        municipalidad = Paragraph(
            f"{self.municipio['NombreMuni']}", estilos["TituloMuni"],)
        titulo = Paragraph(f"PERMISO DE OPERACIÓN",
                           estilos["TituloPrincipal"],)

# TABLA PROPIETARIO
        labels_fila = [
            Paragraph(f"Nombre del Propietario:", estilos["Label"],),
            Paragraph(f""),
            Paragraph(f"Identidad:", estilos["Label"],),
        ]
        valores_fila = [
            Paragraph(f"{self.datos.Propietario}", estilos["Valor"],),
            Paragraph(f""),
            Paragraph(f"{self.datos.idrepresentante}:", estilos["Valor"],)
        ]
        tabla_propitario = Table(
            [labels_fila, valores_fila],
            colWidths=[290, 20, 190],  # ajusta según tus márgenes
        )
        tabla_propitario.setStyle(estilos_tabla2)
# TABLA NEGOCIO
        labels_fila = [
            Paragraph(
                f"Nombre Establecimiento:", estilos["Label"],),
        ]
        valores_fila = [
            Paragraph(f"{self.datos.Negocio}", estilos["Valor"],)
        ]
        tabla_negocio = Table(
            [labels_fila, valores_fila],
            colWidths=[500],  # ajusta según tus márgenes
        )
        tabla_negocio.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            # Fondo gris para valores
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
        ]))
# TABLA RTN
        labels_fila = [
            Paragraph("R.T.N.:", estilos["Label"]),
            Paragraph(f""),
            Paragraph("R.T.M.:", estilos["Label"]),
            Paragraph(f""),
            Paragraph("Fecha Inicio Operaciones:", estilos["Label"]),
        ]
        valores_fila = [
            Paragraph(f"{self.datos.rtn}", estilos["Valor"]),
            Paragraph(f""),
            Paragraph(f"{self.datos.Identidad}", estilos["Valor"]),
            Paragraph(f""),
            Paragraph(f"{self.datos.FechaNac}", estilos["Valor"]),
        ]
        tabla_rtn = Table(
            [labels_fila, valores_fila],
            colWidths=[150, 20, 150, 20, 160],  # ajusta según tus márgenes
        )
        tabla_rtn.setStyle(estilos_tabla)
# TABLA NATURALEZA
        labels_fila = [
            Paragraph(f"Naturaleza Negocio:", estilos["Label"],),
            Paragraph(f""),
            Paragraph(f"Tipo Solicitud:", estilos["Label"],),
        ]
        valores_fila = [
            Paragraph(f"{self.datos.Actividad}", estilos["Valor"],),
            Paragraph(""),
            Paragraph(f"{self.datos.Observacion}", estilos["Valor"],)
        ]
        tabla_naturaleza = Table(
            [labels_fila, valores_fila],
            colWidths=[290, 20, 190],  # ajusta según tus márgenes
        )
        tabla_naturaleza.setStyle(estilos_tabla2)
# TABLA DIRECCION
        labels_fila = [

            Paragraph(f"Direccion:", estilos["Label"],),
            Paragraph(f""),
            Paragraph(f"Telefono:", estilos["Label"],)
        ]
        valores_fila = [
            Paragraph(f"{self.datos.Direccion}", estilos["Valor"],),
            Paragraph(f""),
            Paragraph(f"{self.datos.Telefono}", estilos["Valor"],)
        ]
        tabla_direccion = Table(
            [labels_fila, valores_fila],
            colWidths=[290, 20, 190],  # ajusta según tus márgenes
        )
        tabla_direccion.setStyle(estilos_tabla2)
# TEXTOS
        texto1 = Paragraph(
            "Habiendo cumplido con los requisitos establecidos en el Reglamento que institucionaliza el proceso de emisión y obtención del Permiso de Operación Simplificado, se otorga el presente permiso a:", estilos["parrafo"])
        texto2 = Paragraph(
            "Conforme al Reglamento para la Apertura y Operación de Establecimientos Comerciales en este municipio, el suscrito Jefe del Departamento de Control Tributario concede el presente permiso, el cual deberá colocarse en un lugar visible del establecimiento.", estilos["parrafo"])
        texto3 = Paragraph(
            "Nota: En caso de cierre definitivo del negocio, el titular del permiso deberá presentarse a esta oficina dentro de un plazo máximo de treinta (30) días para notificar dicho cierre y presentar la declaración correspondiente por el tiempo transcurrido hasta la fecha del cierre.", style=estilos["parrafo"])
# FECHA DE EMISION
        ahora = self.datos.Fecha
        dia = ahora.day
        mes = ahora.strftime("%B")
        anio = ahora.year
        valores_fila = [
            Paragraph(f"Emitido a los", estilos["Label"],),
            Paragraph(f"{dia}", estilos["Valor"],),
            Paragraph(f"dias del mes de", estilos["Label"],),
            Paragraph(f"{mes}", estilos["Valor"],),
            Paragraph(f"del año", estilos["Label"],),
            Paragraph(f"{anio}", estilos["Valor"],)
        ]
        tabla_fecha = Table(
            [valores_fila],
            colWidths=[90, 60, 110, 110, 60, 60],  # ajusta según tus márgenes
        )
        tabla_fecha.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            # Fondo gris para valores
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
        ]))
# TABLA QR
        num_permiso = Paragraph(
            f"{self.datos.NoPermiso}",  estilos["NumPermiso"], )

        qr_img = qrcode.make(permiso_datos)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        # crea Flowable Image para ReportLab
        qr_flowable = Image(buffer, width=60, height=60)

# TABLA FIRMA
        if not self.justicia_firma:
            valores_fila = [
                Paragraph("",),
                Paragraph("",),
                Paragraph("Administración Tributaria", estilos["Firma"]),
                Paragraph("",),
                Paragraph("",),
            ]
            tabla_firma = Table(
                [valores_fila],
                colWidths=[50, 100, 200, 100, 50],  # ajusta según tus márgenes
            )
            tabla_firma.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # línea encima de la celda central
                ("LINEABOVE", (2, 0), (2, 0), 1, "black"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
        else:
            valores_fila = [
                Paragraph("",),
                Paragraph("Administración Tributaria", estilos["Firma"]),
                Paragraph("",),
                Paragraph("Justicia Municipal", estilos["Firma"]),
                Paragraph("",),
            ]

            tabla_firma = Table(
                [valores_fila],
                colWidths=[20, 210, 20, 210, 20],  # ajusta según tus márgenes
            )
            tabla_firma.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # línea encima de Administración Tributaria
                ("LINEABOVE", (1, 0), (1, 0), 1, "black"),
                # línea encima de Justicia Municipal
                ("LINEABOVE", (3, 0), (3, 0), 1, "black"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
# TABLA ENCABEZADO
        valores_fila = [
            Paragraph(""),
            titulo,
            qr_flowable
        ]
        tabla_titulo = Table(
            [valores_fila],
            colWidths=[100, 300, 100],  # ajusta según tus márgenes
        )
        tabla_titulo.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            # Fondo gris para valores
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
        ]))

        elementos.append(municipalidad)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_titulo)
        linea = HRFlowable(width="80%", thickness=1,
                           color=colors.black, spaceBefore=10, spaceAfter=10)
        elementos.append(linea)
        elementos.append(num_permiso)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_propitario)
        elementos.append(Spacer(1, 5))
        elementos.append(texto1)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_negocio)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_rtn)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_naturaleza)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_direccion)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_fecha)
        elementos.append(Spacer(1, 5))
        elementos.append(texto2)
        elementos.append(Spacer(1, 5))
        elementos.append(texto3)
        elementos.append(Spacer(1, 30))
        elementos.append(tabla_firma)
        elementos.append(Spacer(1, 5))
        footer = Paragraph(
            f"<b>Valido hasta el 31 de Diciembre del año {self.datos.Periodo}</b>",  estilos["Label"], )
        elementos.append(footer)

        doc.build(elementos)
