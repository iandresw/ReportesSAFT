from flet import Container, Row, Text, Offset, Animation, AnimationCurve, MainAxisAlignment, Icon, Icons, FontWeight, TextAlign, Padding, TextField, TextStyle
from ui.ui_colors import color_borde, color_bg, color_texto


borde_color = color_borde()
bg_color = color_bg()
text_color = color_texto()
text_sise = 10
alto_textFiel = 40
color_card_verde = '#1BAE70'


def crear_text_var_navigation(self, Value="text_barra_navigtion",
                              offset=Offset(0, 0),
                              bgcolor=None,
                              animate_offset=Animation(
                                  500, AnimationCurve.EASE_IN_OUT_QUAD),
                              on_change_page_click=None,
                              icon=Icons.PERSON_ADD_ALT):
    return Container(
        padding=10,
        bgcolor=bg_color,
        border_radius=15,
        offset=offset,
        animate_offset=animate_offset,
        on_click=lambda e: on_change_page_click(
            e) if on_change_page_click else None,
        height=40,
        content=Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Icon(icon, color="white"),
                Text(Value, width=120)
            ]
        )
    )


def text_mensaje():
    return Text("", size=12.5, color=borde_color, width=500)


def txt_label_text(text=''):
    return Container(
        padding=Padding(left=10, right=0, top=10, bottom=0),
        col=8,
        content=Text(text, size=12.5, color=borde_color, width=500,
                     col=12, weight=FontWeight.W_400, text_align=TextAlign.START,)
    )


def create_texFiel_fijas(label_text="", visible=True, read_only=True, width=None):
    return TextField(
        label=label_text,
        expand=True,
        border_radius=10,
        width=width,
        height=alto_textFiel,
        text_size=text_sise,
        visible=visible,
        col=2,
        text_align=TextAlign.CENTER,
        read_only=read_only,
        bgcolor=color_bg(),
        border_color=borde_color,
        label_style=TextStyle(
            size=text_sise, font_family="Tahoma", color=text_color, weight=FontWeight.W_400,),
        text_style=TextStyle(size=text_sise, font_family="Tahoma", color=text_color, weight=FontWeight.W_400,),)
