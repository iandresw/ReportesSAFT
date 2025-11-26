from flet import ElevatedButton, ButtonStyle, TextStyle, Alignment, TextAlign, Colors, Border, BorderSide, Container, RoundedRectangleBorder
from ui.ui_colors import color_bg_2, color_bg, color_borde, color_shadow, color_texto


def create_boton(text_label="hola", on_click=None, width=200, disabled=None):
    borde_color = color_borde()
    txt_color = color_texto()
    shadow_color = color_shadow()
    return ElevatedButton(
        text=text_label,
        disabled=disabled,
        width=width,
        color=txt_color,
        style=ButtonStyle(
            side=BorderSide(2, borde_color),
            shape=RoundedRectangleBorder(radius=18),
            bgcolor=color_bg_2(),
            shadow_color=shadow_color,
            text_style=TextStyle(size=10, font_family="Tahoma"),
        ),
        on_click=on_click,
    )
