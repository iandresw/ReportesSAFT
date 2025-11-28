from flet import Container, Row, Text, Offset, Animation, TextField, IconButton, InputBorder, AnimationCurve, MainAxisAlignment, Icon, Icons, FontWeight, TextAlign, Padding, TextField, TextStyle
from ui.ui_colors import color_borde, color_bg, color_texto, color_icon_loguin


borde_color = color_borde()
bg_color = color_bg()
text_color = color_texto()
icon_color = color_icon_loguin()
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


def create_texFiel_fijas(label_text="", visible=True, read_only=True, width=None, ref=None) -> TextField:
    return TextField(
        label=label_text,
        expand=True,
        border_radius=10,
        width=width,
        ref=ref,
        height=alto_textFiel,
        text_size=text_sise,
        visible=visible,
        col=2,
        text_align=TextAlign.CENTER,
        read_only=read_only,
        bgcolor=color_bg(),
        border_color=borde_color,
        label_style=TextStyle(size=text_sise, font_family="Tahoma",
                              color=text_color, weight=FontWeight.W_400,),
        text_style=TextStyle(size=text_sise, font_family="Tahoma", color=text_color, weight=FontWeight.W_400,),)


def text_usuario() -> TextField:
    return TextField(
        width=280,
        height=40,
        hint_text='Usuario SAFT',
        border=InputBorder.UNDERLINE,
        color=icon_color,
        text_style=TextStyle(color=icon_color),
        prefix_icon=Icon(Icons.PERSON_2, color=icon_color),
        label_style=TextStyle(color=icon_color, font_family="Tahoma",),
    )


def text_usuario_password() -> TextField:

    return TextField(
        width=280,
        height=40,
        hint_text='Contraseña',
        border=InputBorder.UNDERLINE,
        text_style=TextStyle(color=icon_color),
        color=icon_color,
        prefix_icon=Icon(Icons.LOCK, color=icon_color),
        can_reveal_password=True,
        password=True,
        suffix_style=TextStyle(color=icon_color, size=20),
    )


def create_titulo_modal(tiulo: str) -> Text:
    return Text(
        value=tiulo,
        color=color_texto(),
        font_family="Tahoma",
        text_align=TextAlign.CENTER,
        size=15
    )


def create_sub_titulo_modal(sub_tiulo: str) -> Text:
    return Text(
        value=sub_tiulo,
        color=color_texto(),
        font_family="Tahoma",
        text_align=TextAlign.CENTER,
        size=10
    )
