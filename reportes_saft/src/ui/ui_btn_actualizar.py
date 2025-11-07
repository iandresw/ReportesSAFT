from flet import Page, ElevatedButton, Icons, ButtonStyle, TextStyle, Alignment, TextAlign, Colors, Border, BorderSide, Container
from ui.ui_colors import color_bg, color_borde, color_shadow, color_texto


def create_update_button(page: Page, on_click=None):
    return Container(
        border=Border(top=BorderSide(2, Colors.BLUE_700), right=BorderSide(
            2, Colors.BLUE_700), left=BorderSide(2, Colors.BLUE_700), bottom=BorderSide(2, Colors.BLUE_700)),
        border_radius=18,
        content=ElevatedButton(
            text="Actualizar aplicación",
            icon=Icons.SYSTEM_UPDATE,
            color=Colors.BLUE_700,
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
