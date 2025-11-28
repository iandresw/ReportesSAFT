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
