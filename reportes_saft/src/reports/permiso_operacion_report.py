from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
from models.tra_permop import Tra_PermOpe
from ui.ui_style_table import table_style, columa_style
from datetime import datetime
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

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
    print("⚠️ Advertencia: no se encontraron las fuentes Malgun en /fonts/")


class PermisoOperacionReport:
    def __init__(self, datos: Tra_PermOpe, municipio, titulo_reporte):
        self.datos = datos
        self.municipio = municipio
        self.titulo = titulo_reporte

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=letter)
        elementos = []

        estilos = StyleSheet1()

        estilos.add(ParagraphStyle(
            name='TituloMuni',
            fontSize=36,
            alignment=1,  # centrado
            leading=35,
            spaceAfter=10,
            fontName="Malgun-Bold"
        ))

        estilos.add(ParagraphStyle(
            name='TituloPrincipal',
            fontSize=20,
            textColor=colors.black,
            alignment=1,  # centrado
            fontName="Jhenghei",
            spaceAfter=20
        ))

        estilos.add(ParagraphStyle(
            name='Label',
            fontSize=12,
            textColor=colors.green,
            fontName="GOTHICB",
            leading=14,
            spaceBefore=6
        ))

        estilos.add(ParagraphStyle(
            name='Valor',
            fontSize=11,
            textColor=colors.black,
            fontName="GOTHICB",
            backColor=colors.whitesmoke,  # Fondo gris claro
            leftIndent=8,
            borderWidth=50,
            rightIndent=8,
            leading=14
        ))

        estilos.add(ParagraphStyle(
            name='Texto',
            fontSize=11,
            textColor=colors.black,
            fontName="Century-Gothic",
            leading=15,
            alignment=4,  # justificado
            spaceBefore=10,
            spaceAfter=10
        ))

        municipalidad = Paragraph(
            f"{self.municipio['NombreMuni']}", estilos["TituloMuni"],)
        titulo = Paragraph(f"PERMISO DE OPERACIÓN",
                           estilos["TituloPrincipal"],)

        label_propietario = Paragraph(
            f"Nombre del Propietario:", estilos["Label"],)
        label_identidad = Paragraph(f"Identidad:", estilos["Label"],)
        label_negocio = Paragraph(
            f"Nombre Establecimiento:", estilos["Label"],)
        labels_fila = [
            Paragraph("R.T.N.:", estilos["Label"]),
            Paragraph("R.T.M.:", estilos["Label"]),
            Paragraph("Fecha Inicio Operaciones:", estilos["Label"]),
        ]
        valores_fila = [
            Paragraph(f"{self.datos.rtn}", estilos["Valor"]),
            Paragraph(f"{self.datos.Identidad}", estilos["Valor"]),
            Paragraph(f"{self.datos.FechaNac}", estilos["Valor"]),
        ]
        tabla_rtn = Table(
            [labels_fila, valores_fila],
            colWidths=[150, 150, 200],  # ajusta según tus márgenes
        )
        tabla_rtn.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            # Fondo gris para valores
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
        ]))
        label_naturaleza = Paragraph(
            f"Naturaleza Negocio:", estilos["Label"],)
        label_tipo_sol = Paragraph(f"Tipo Solicitud:", estilos["Label"],)
        label_direccion = Paragraph(f"Direccion:", estilos["Label"],)

        label_telefono = Paragraph(f"Telefono:", estilos["Label"],)

        texto1 = Paragraph("Conforme al Reglamento para la Apertura y Operación de Establecimientos Comerciales en este municipio, el suscrito Jefe del Departamento de Control Tributario concede el presente permiso, el cual deberá colocarse en un lugar visible del establecimiento.")
        texto2 = Paragraph(
            "Habiendo cumplido con los requisitos establecidos en el Reglamento que institucionaliza el proceso de emisión y obtención del Permiso de Operación Simplificado, se otorga el presente permiso a:")

        num_permiso = Paragraph(
            f"{self.datos.NoPermiso}",  estilos["Valor"], )
        propietario = Paragraph(
            f"{self.datos.Propietario}", estilos["Valor"],)
        identidad = Paragraph(
            f"{self.datos.idrepresentante}:", estilos["Valor"],)
        negocio = Paragraph(f"{self.datos.Negocio}", estilos["Valor"],)

        naturaleza = Paragraph(f"{self.datos.Actividad}", estilos["Valor"],)
        tipo_sol = Paragraph(f"{self.datos.Observacion}", estilos["Valor"],)
        direccion = Paragraph(f"{self.datos.Direccion}", estilos["Valor"],)
        telefono = Paragraph(f"{self.datos.Telefono}", estilos["Valor"],)

        elementos.append(municipalidad)
        elementos.append(titulo)
        elementos.append(num_permiso)
        elementos.append(Spacer(1, 12))
        elementos.append(label_propietario)
        elementos.append(propietario)
        elementos.append(Spacer(1, 12))
        elementos.append(texto1)
        elementos.append(Spacer(1, 12))
        elementos.append(label_identidad)
        elementos.append(identidad)
        elementos.append(Spacer(1, 12))
        elementos.append(label_negocio)
        elementos.append(negocio)
        elementos.append(Spacer(1, 12))
        elementos.append(label_naturaleza)
        elementos.append(naturaleza)
        elementos.append(Spacer(1, 12))

        # Aquí insertamos la tabla
        elementos.append(tabla_rtn)
        elementos.append(Spacer(1, 12))
        elementos.append(Spacer(1, 12))
        elementos.append(label_naturaleza)
        elementos.append(naturaleza)
        elementos.append(Spacer(1, 12))
        elementos.append(label_tipo_sol)
        elementos.append(tipo_sol)
        elementos.append(Spacer(1, 12))
        elementos.append(label_direccion)
        elementos.append(direccion)
        elementos.append(Spacer(1, 12))
        elementos.append(label_telefono)
        elementos.append(telefono)
        elementos.append(Spacer(1, 12))
        elementos.append(texto2)

        footer = Paragraph(
            "<b>Generado por el sistema SAFT</b>",  estilos["Label"], )
        elementos.append(footer)

        doc.build(elementos)
