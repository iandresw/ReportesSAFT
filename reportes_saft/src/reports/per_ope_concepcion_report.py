from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.fonts import addMapping
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable, Image
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from models.tra_permop import Tra_PermOpe
from ui.ui_style_table import estilos_parrafo
import os
import locale
import json
import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas


for loc in ["es_ES", "Spanish", "es-ES", "es_HN", "es_ES.UTF-8"]:
    try:
        locale.setlocale(locale.LC_TIME, loc)
        break
    except locale.Error:
        pass


class PerOpeConcepcionReport:
    def __init__(self, datos: Tra_PermOpe, municipio, titulo_reporte, firma_justicia=False, municipio_admin=False):
        self.datos = datos
        self.municipio = municipio
        self.titulo = titulo_reporte
        self.justicia_firma = firma_justicia
        self.muni_admin = municipio_admin
        self.margen = 1.27 * cm

    def dibujar_borde(self, canvas, doc):
        w, h = landscape(letter)

        margen = 10  # borde separado 10px del borde real

        canvas.saveState()
        canvas.setLineWidth(3)
        canvas.setStrokeColor(colors.gray)

        # borde exterior
        canvas.rect(
            margen,
            margen,
            w - 2 * margen,
            h - 2 * margen
        )

        # borde interno decorativo
        canvas.setLineWidth(1.5)
        canvas.setStrokeColor(colors.lightblue)
        canvas.rect(
            margen + 10,
            margen + 10,
            w - 2 * (margen + 10),
            h - 2 * (margen + 10)
        )

        canvas.restoreState()

    def generar_pdf(self, ruta_salida="mora_bi_report.pdf"):
        doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(letter),
                                leftMargin=self.margen,
                                rightMargin=self.margen,
                                topMargin=self.margen,
                                bottomMargin=self.margen)
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
        ahora = self.datos.Fecha
        dia = ahora.day
        mes = ahora.strftime("%B")
        anio = ahora.year

        municipalidad = Paragraph(
            f"{self.muni_admin["NombreEmpresa"].upper()}", estilos["concepcion_title"],)
        email = Paragraph(
            f"E-Mail: {self.municipio["Email"].lower()}, Tel.{self.municipio["Telefono"]}", estilos["concepcion_telefono"],)

        titulo_po = Paragraph(
            f"PERMISO DE APERTURA Y OPERACIÓN DEL NEGOCIO", estilos["concepcion_title_ope"],)
        fila_titulo_per = [titulo_po]
        tabla_titulo_po = Table([fila_titulo_per], colWidths=[700])
        estilo = TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOX", (0, 0), (0, 0), 0.8, colors.grey),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
        tabla_titulo_po.setStyle(estilo)

        texto1 = Paragraph(
            f"POR ESTE MEDIO SE HACE CONSTAR QUE: EL PROPIETARIO DEL ESTABLECIMIENTO A CONTINUACIÓN DETALLADO, ESTA AUTORIZADO PARA OPERAR EL SIGUIENTE NEGOCIO.", estilos["concepcion_parrafo"])

        fila_texto1 = [
            texto1
        ]
        tabla_texto1 = Table([fila_texto1], colWidths=[700])
        tabla_texto1.setStyle(estilo)


# TABLA PROPIETARIO
        fila_propitario = [
            Paragraph(f"Nombre del propietario o Rep. Legal:",
                      estilos["concepcion_campos"],),
            Paragraph(f"{self.datos.Propietario}",
                      estilos["concepcion_campos"]),
        ]
        fila_dni = [
            Paragraph(f"ID Nº: ", estilos["concepcion_campos"],),
            Paragraph(f"{self.datos.idrepresentante}",
                      estilos["concepcion_campos"]),
        ]
        fila_negocio = [
            Paragraph(f"Nombre Empresa:", estilos["concepcion_campos"],),
            Paragraph(f"{self.datos.Negocio}", estilos["concepcion_campos"],),
        ]
        fila_ubicacion = [
            Paragraph(f"Ubicacion:", estilos["concepcion_campos"],),
            Paragraph(f"{self.datos.Direccion}",
                      estilos["concepcion_campos"],),
        ]
        fila_actividad = [
            Paragraph(f"Tipo de Actividad:", estilos["concepcion_campos"],),
            Paragraph(f"{self.datos.Actividad}",
                      estilos["concepcion_campos"],),
        ]
        fila_fecha_vence = [
            Paragraph(f"Fecha Vencimiento:", estilos["concepcion_campos"],),
            Paragraph(f"31 de Diciembre del año {self.datos.Periodo}",
                      estilos["concepcion_campos"],),
        ]
        fila_no_recibo = [
            Paragraph(f"Serie de recibo de pago No.:",
                      estilos["concepcion_campos"],),
            Paragraph(f"{self.datos.NumRecibo}",
                      estilos["concepcion_campos"],),
        ]
        lugar_fecha = ""
        fila_lugar_fecha = [Paragraph(f"{self.municipio["NombreMuni"].capitalize()}, {self.municipio["NombreDepto"].capitalize()} a los {dia} dias del mes de {mes} del {anio}", estilos["concepcion_campos"]),

                            ""]


# TABLA NEGOCIO

        tabla_datos = Table(
            [fila_propitario, fila_dni, fila_negocio, fila_ubicacion,
                fila_actividad, fila_fecha_vence, fila_no_recibo, fila_lugar_fecha],
            colWidths=[300, 400]
        )

        estilo = TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("SPAN", (0, 7), (1, 7)),  # Combina columnas 0 a 2 en la fila 1
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            # línea arriba del header
            ("BOX", (0, 0), (-1, -1), 1, colors.grey),  # borde exterior

            # Líneas horizontales internas (filas)
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            # Fondo gris para valores
            ("BACKGROUND", (0, 1), (0, -1), colors.transparent),
            ("BACKGROUND", (1, 1), (1, -1), colors.transparent),
        ])
        tabla_datos.setStyle(estilo)


# TEXTOS

        BASE_DIR = os.path.dirname(os.path.abspath(
            __file__))   # carpeta donde está el .py
        # sube un nivel → assets
        ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")

        logo_mun = Image(os.path.join(ASSETS_DIR, "logo_concepcion.png"), width=(
            5.84*cm), height=(3.52*cm))
        escudo_nac = Image(os.path.join(
            ASSETS_DIR, "logo_escudo_mini.png"), width=(2.37*cm), height=(3.46*cm))


# TABLA QR

        fila_tirulo = [

            logo_mun,
            None,
            municipalidad,
            None,
            escudo_nac,

        ]
        tabla_encabezado = Table(
            [fila_tirulo],
            colWidths=[100, 50, 300, 50, 100],  # ajusta según tus márgenes
        )
        tabla_encabezado.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            # (Opcional) Líneas de prueba
            # ('GRID', (0,0), (-1,-1), 0.5, colors.red)
        ]))

        qr_img = qrcode.make(permiso_datos)
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        # crea Flowable Image para ReportLab
        qr_flowable = Image(buffer, width=60, height=60)
        fila_pie = [
            Paragraph(f"COLOCAR EN SITIO VISIBLE",
                      estilos["concepcion_num_ope"]),
            None,
            Paragraph(f"No. {self.datos.NoPermiso}",
                      estilos["concepcion_num_ope"])
        ]

        tabla_pie = Table(
            [fila_pie],
            colWidths=[300, 200, 200],  # ajusta según tus márgenes
        )
        tabla_pie.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOX", (0, 0), (0, 0), 0.8, colors.grey),
            ("BOX", (2, 0), (2, 0), 0.8, colors.grey),
        ]))


# TABLA FIRMA
        valores_fila_CAMPO1 = [
            qr_flowable,
            None,
            None,
            None,
        ]
        valores_fila_CAMPO2 = [
            None,
            None,
            None,
            None,
        ]
        valores_fila_CAMPO3 = [
            None,
            None,
            None,
            None,
        ]
        valores_fila = [
            None,
            Paragraph(f"{self.muni_admin["Alcalde"]}",
                      estilos["concepcion_campos_firma"]),
            Paragraph(f"{self.muni_admin["Administrador"]}",
                      estilos["concepcion_campos_firma"]),
            Paragraph(f"{self.muni_admin["Tributaria"]}",
                      estilos["concepcion_campos_firma"]),
        ]
        valores_fila_1 = [
            None,
            Paragraph("Alcalde Municipal", estilos["concepcion_campos_firma"]),
            Paragraph("Juez de Policía", estilos["concepcion_campos_firma"]),
            Paragraph("Administración Tributaria",
                      estilos["concepcion_campos_firma"]),
        ]

        tabla_firma = Table(
            [valores_fila_CAMPO1, valores_fila_CAMPO2,
                valores_fila_CAMPO3, valores_fila, valores_fila_1],
            colWidths=[100,  200,  200, 200],  # ajusta según tus márgenes
        )
        tabla_firma.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ('SPAN', (0, 0), (0, -1)),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEABOVE", (1, 3), (-1, 3), 1, colors.grey),
            ("BOX", (1, 0), (1, -1), 0.8, colors.grey),
            ("BOX", (2, 0), (2, -1), 0.8, colors.grey),
            ("BOX", (3, 0), (3, -1), 0.8, colors.grey),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))

        elementos.append(tabla_encabezado)
        elementos.append(email)
        elementos.append(tabla_titulo_po)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_texto1)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_datos)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_firma)
        elementos.append(Spacer(1, 5))
        elementos.append(tabla_pie)
        elementos.append(Spacer(1, 5))
        doc.build(
            elementos,
            onFirstPage=self.dibujar_borde,
            onLaterPages=self.dibujar_borde
        )
