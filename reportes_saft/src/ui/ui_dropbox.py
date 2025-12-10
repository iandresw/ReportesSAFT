from flet import Dropdown, dropdown, TextStyle, ButtonStyle
from ui.ui_colors import color_check, color_texto, color_bg_2, color_borde


def dropbox_aldeas(aldeas: list[dict], ref):
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    return Dropdown(
        ref=ref,
        label="Seleccione la aldea",
        width=300,
        options=[dropdown.Option(
            key=str(a["CodAldea"]),
            text=a["NombreAldea"],
            text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color)))
            for a in aldeas],
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color))


def horas(label="Hora") -> Dropdown:
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    horas = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
             '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',]
    return Dropdown(
        label=label,
        options=[dropdown.Option(h, text_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color))) for h in horas],
        width=100,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color)
    )


def dias():
    texto_color = color_texto()
    border_color = color_borde()
    bg_color = color_bg_2()
    dias = ["LUNES", 'MARTES', 'MIERCOLES',
            'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']
    return Dropdown(
        label="Dias",
        options=[dropdown.Option(m, text_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
            style=ButtonStyle(color=texto_color, text_style=TextStyle(
                size=10, font_family="Tahoma", color=texto_color))) for m in dias],
        width=100,
        color=texto_color,
        border_color=border_color,
        bgcolor=bg_color,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=texto_color),
        text_style=TextStyle(size=10, font_family="Tahoma", color=texto_color)
    )
