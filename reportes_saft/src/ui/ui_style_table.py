from reportlab.platypus import TableStyle, Paragraph, Spacer
from ui.ui_colors import color_bg, color_borde, color_shadow, color_texto
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def table_style():
    return TableStyle(
        [
            # Encabezado
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            # Bordes y fondo general
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            # 🔹 Alineaciones personalizadas por columna
            # Primera a la izquierda
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            # Segunda columna en el centro
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            # Tercera columna en el centro
            ("ALIGN", (2, 0), (2, -1), "CENTER"),
            # Cuarta columna en el centro
            ("ALIGN", (3, 0), (3, -1), "CENTER"),
            # Quinta columna en el centro
            ("ALIGN", (4, 0), (4, -1), "CENTER"),
        ]
    )


def columa_style():
    return ParagraphStyle(
        name="TablaColumnas",
        textColor=colors.white,
        fontName="Helvetica",
        fontSize=8,
        leading=10,   # espacio entre líneas
        alignment=1,  # 0=izq, 1=centro, 2=derecha
    )
