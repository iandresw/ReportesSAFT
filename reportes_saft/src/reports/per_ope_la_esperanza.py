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
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas


def add_background(canvas, doc, image_path):
    # Dimensiones de media carta en puntos (pulgadas * 72)
    width, height = letter  # Página completa letter
    half_height = height / 2  # Media carta, horizontalmente en vertical
    canvas.drawImage(
        image_path,
        0, 0,  # origen en la parte superior
        width=width,
        height=458.64,
        preserveAspectRatio=True,
        mask='auto'
    )


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
font_arial_rounded_mt = os.path.join(
    FONTS_DIR, "Arial-Rounded-MT-Bold-Bold.ttf")
font_arial_unicode_ms = os.path.join(FONTS_DIR, "Arial-Unicode-MS-Regular.ttf")
font_britannic_bold = os.path.join(FONTS_DIR, "Britannic-Bold-Bold.ttf")
# Registrar fuentes si existen
# Registrar fuentes si existen
if os.path.exists(font_regular):
    pdfmetrics.registerFont(TTFont('Malgun', font_regular))
    addMapping('Malgun', 0, 0, 'Malgun')  # Normal

if os.path.exists(font_bold):
    pdfmetrics.registerFont(TTFont('Malgun-Bold', font_bold))
    addMapping('Malgun', 1, 0, 'Malgun-Bold')  # Bold

if os.path.exists(font_GOTHICB):
    pdfmetrics.registerFont(TTFont('GOTHICB', font_GOTHICB))
    addMapping('GOTHICB', 1, 0, 'GOTHICB')  # Bold

if os.path.exists(font_GOTHICB0):
    pdfmetrics.registerFont(TTFont('GOTHICB0', font_GOTHICB0))
    addMapping('GOTHICB', 0, 0, 'GOTHICB0')  # Regular

if os.path.exists(font_arial_rounded_mt):
    pdfmetrics.registerFont(
        TTFont('Arial-Rounded-MT-Bold', font_arial_rounded_mt))
    addMapping('Arial-Rounded-MT', 1, 0, 'Arial-Rounded-MT-Bold')

if os.path.exists(font_arial_unicode_ms):
    pdfmetrics.registerFont(TTFont('Arial-Unicode-MS', font_arial_unicode_ms))
    addMapping('Arial-Unicode', 0, 0, 'Arial-Unicode-MS')

if os.path.exists(font_britannic_bold):
    pdfmetrics.registerFont(TTFont('Britannic-Bold', font_britannic_bold))
    addMapping('Britannic', 1, 0, 'Britannic-Bold')


class PerOpeLaEsperanzaReport:
    def __init__(self, datos: Tra_PermOpe, municipio, titulo_reporte, firma_justicia=False):
        self.datos = datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.justicia_firma = firma_justicia

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=(612, 460),
                                leftMargin=40,
                                rightMargin=40,
                                topMargin=50,
                                bottomMargin=0)
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

        municipalidad = Paragraph(
            f"ALCALDIA MUNICIPAL DE LA ESPERANZA", estilos["la_esperanza_title"],)
        titulo = Paragraph(
            f"LA ESPERANZA, INTIBUCA HONDURAS C.A.", estilos["la_esperanza_title"],)
        titulo_po = Paragraph(
            f"PERMISO DE OPERACIÓN DE NEGOCIOS {self.datos.Periodo}", estilos["la_esperanza_title_ope"],)
        telefonos = Paragraph(
            f"TELEFONO: 2783-1818, 2783-1296 ", estilos["la_esperanza_telefono"],)

# TABLA PROPIETARIO
        fila_negocio = [
            Paragraph(f"NOMBRE DEL NEGOCIO:", estilos["la_esperanza_campos"],),
            Paragraph(f""),
            Paragraph(f"{self.datos.Negocio}",
                      estilos["la_esperanza_campos"],),
        ]
        fila_rtn = [
            Paragraph(f"RTN:", estilos["la_esperanza_campos"],),
            Paragraph(f""),
            Paragraph(f"{self.datos.rtn}", estilos["la_esperanza_campos"]),
        ]
        fila_propitario = [
            Paragraph(f"PROPIETARIO:", estilos["la_esperanza_campos"],),
            Paragraph(f""),
            Paragraph(f"{self.datos.Propietario}",
                      estilos["la_esperanza_campos"]),
        ]
        fila_ubicacion = [
            Paragraph(f"UBICACION:", estilos["la_esperanza_campos"],),
            Paragraph(f""),
            Paragraph(f"{self.datos.Direccion}",
                      estilos["la_esperanza_campos"],),
        ]
        fila_actividad = [
            Paragraph(f"ACTIVIDAD PRINCIPAL:",
                      estilos["la_esperanza_campos"],),
            Paragraph(f""),
            Paragraph(f"{self.datos.Actividad}",
                      estilos["la_esperanza_campos"],),
        ]

        fila_footer = [
            Paragraph(
                f"Valido hasta el 31 de Diciembre del año {self.datos.Periodo}", estilos["la_esperanza_parrafo"]),
            Paragraph(""),
            Paragraph(f"NO NEGOCIABLE", estilos["la_esperanza_parrafo"]),
            Paragraph(""),
            Paragraph(f"NOTA: Sin firma y sin sello no es valido.",
                      estilos["la_esperanza_parrafo"]),
        ]

# TABLA NEGOCIO

        tabla_datos = Table(
            [fila_negocio, fila_rtn, fila_propitario,
                fila_ubicacion, fila_actividad],
            colWidths=[180, 20, 300]
        )
        footer = Table(
            [fila_footer],
            colWidths=[200, 20, 100, 20, 200]
        )
        estilo = TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            # Fondo gris para valores
            ("BACKGROUND", (0, 1), (0, -1), colors.transparent),
            ("BACKGROUND", (1, 1), (1, -1), colors.transparent),
        ])
        tabla_datos.setStyle(estilo)

        ahora = self.datos.Fecha
        dia = ahora.day
        mes = ahora.strftime("%B")
        anio = ahora.year


# TEXTOS
        texto1 = Paragraph(
            f"De acuerdo al artículo N.124 del reglamento de la ley de Municipalidades, para la apertura y operación de establecimientos comerciales en este Municipio, el suscrito Alcalde Municipal concede el presente permiso el cual deberá ser colocado en un sitio visible. Dado en la ciudad de la Esperanza, Departamento de Intibucá, a los {dia} días del mes de {mes} del año {anio}. ", estilos["la_esperanza_parrafo"])

# TABLA QR
        num_permiso = Paragraph(
            f"{self.datos.NoPermiso}", estilos["la_esperanza_num_ope"])

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
                Paragraph("Dr. Miguel Antonio Fajardo Mejia",
                          estilos["la_esperanza_campos_firma"]),
                Paragraph("",),
                Paragraph("P.M. Luz Marina Hernández",
                          estilos["la_esperanza_campos_firma"]),
                Paragraph("",),
            ]
            valores_fila_1 = [
                Paragraph("",),
                Paragraph("ALCALDE MUNICIPAL",
                          estilos["la_esperanza_campos_firma"]),
                Paragraph("",),
                Paragraph("TESORERA MUNICIPAL",
                          estilos["la_esperanza_campos_firma"]),
                Paragraph("",),
            ]
            tabla_firma = Table(
                [valores_fila, valores_fila_1],
                colWidths=[20, 150, 40, 150, 20],  # ajusta según tus márgenes
            )
            tabla_firma.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # línea encima de la celda central
                ("LINEABOVE", (1, 0), (1, 0), 1, "black"),
                ("LINEABOVE", (3, 0), (3, 0), 1, "black"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
        else:
            valores_fila = [
                Paragraph("ALCALDE MUNICIPAL",
                          estilos["la_esperanza_campos_firma"]),
                Paragraph(""),
                Paragraph("DIRECCIÓN DE JUSTICIA MUNICIPAL",
                          estilos["la_esperanza_campos_firma"]),
                Paragraph(""),
                Paragraph("TESORERA MUNICIPAL",
                          estilos["la_esperanza_campos_firma"]),
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
                ("LINEABOVE", (0, 0), (0, 0), 1, "black"),
                ("LINEABOVE", (2, 0), (2, 0), 1, "black"),
                ("LINEABOVE", (4, 0), (4, 0), 1, "black"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
        elementos.append(num_permiso)
        elementos.append(municipalidad)

        elementos.append(titulo)
        elementos.append(telefonos)
        elementos.append(titulo_po)

        linea = HRFlowable(width="80%", thickness=1,
                           color=colors.black, spaceBefore=10, spaceAfter=10)
        # elementos.append(linea)
        elementos.append(Spacer(1, 10))
        elementos.append(tabla_datos)

        elementos.append(texto1)

        elementos.append(footer)
        elementos.append(Spacer(1, 40))
        elementos.append(tabla_firma)
        background_image = os.path.join(
            BASE_DIR, "..", "assets", "per_ope_la_esperanza.png")
        doc.build(elementos,
                  onFirstPage=lambda canvas, doc: add_background(
                      canvas, doc, background_image),
                  onLaterPages=lambda canvas, doc: add_background(
                      canvas, doc, background_image),
                  )
