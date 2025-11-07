from flet import ElevatedButton, ButtonStyle, TextStyle, Alignment, TextAlign, Colors, Border, BorderSide, Container
from ui.ui_colors import color_bg, color_borde, color_shadow, color_texto


def create_boton(text_label="hola", on_click=None):
    return Container(
        border=Border(top=BorderSide(2, color_borde()), right=BorderSide(
            2, color_borde()), left=BorderSide(2, color_borde()), bottom=BorderSide(2, color_borde())),
        border_radius=18,
        content=ElevatedButton(
            text=text_label,
            color=color_texto(),
            width=200,
            style=ButtonStyle(bgcolor=color_bg(),
                              # overlay_color='#E06C75',
                              shadow_color=color_shadow(),
                              text_style=TextStyle(
                                  size=10,
                                  italic=False,
                                  font_family="Tahoma",
            ), alignment=Alignment(0, 0)),
            on_click=on_click)
    )
