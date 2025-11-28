from flet import Radio, TextStyle, RadioGroup, Column, ScrollMode, MainAxisAlignment, CrossAxisAlignment, Row
from ui.ui_colors import color_check, color_texto


def create_radio(value='0', label_text="") -> Radio:
    return Radio(value=value,
                 label=label_text,
                 fill_color=color_check(),
                 label_style=TextStyle(
                     size=10, color=color_texto(), font_family="Tahoma")
                 )


def rd_tipo_factura(tipo_impuesto):
    return RadioGroup(
        ref=tipo_impuesto,
        value="0,1,2,3,4,5,7",
        content=Column([
            create_radio(value="0", label_text="Otras Tasas"),
            create_radio(value="1", label_text="Bienes Inmuebles"),
            create_radio(value="4", label_text="Impuesto Personal"),
            create_radio(
                value="2,3", label_text="Industria, Comercio y Servicio"),
            create_radio(value="5", label_text="Servicios Públicos"),
            create_radio(value="7", label_text="Planes de Pago"),
            create_radio(value="0,1,2,3,4,5,7", label_text="Todos (General)")
        ],)
    )


def rd_ubicacion(ubicacion):
    return RadioGroup(
        ref=ubicacion,
        value="0",
        content=Row([
            create_radio(value="0", label_text="Urbano"),
            create_radio(value="1", label_text="Rural"),
        ], alignment=MainAxisAlignment.SPACE_AROUND)
    )
