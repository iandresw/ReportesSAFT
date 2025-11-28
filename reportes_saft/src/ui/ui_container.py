from flet import (Container, Animation, AnimationCurve, TextStyle, Offset,   alignment,  # type: ignore
                  Column, BoxShadow, Text, Colors, CrossAxisAlignment, MainAxisAlignment, ScrollMode, Row, Icon, Border, BorderSide, ShadowBlurStyle)

from ui.ui_colors import color_border_contenedor, color_bg, container_color, color_shadow, color_bg_2, color_texto


animation_style = Animation(500, AnimationCurve.EASE_IN_TO_LINEAR)


def create_container(controls=[], col=1, width=None, height=None, expand=None, content=None, alineacion_col=None) -> Container:
    if content:
        content = content
    else:
        content = Column(controls=controls,
                         scroll=ScrollMode.AUTO,
                         col=12,
                         alignment=MainAxisAlignment.CENTER,         # centra verticalmente
                         horizontal_alignment=CrossAxisAlignment.CENTER,  # centra horizontalmente
                         expand=True)
    return Container(
        bgcolor=color_bg_2(),
        # alignment=alignment.center,
        expand=expand,
        col=col,
        border_radius=10,
        # border=Border(
        #     top=BorderSide(0.5, color_border_contenedor()),
        #     right=BorderSide(0.5, color_border_contenedor()),
        #     bottom=BorderSide(0.5, color_border_contenedor()),
        #     left=BorderSide(0.5, color_border_contenedor())),

        padding=10,

        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=color_bg_2(),
            offset=Offset(0, 0),
            blur_style=ShadowBlurStyle.SOLID,
        ),
        content=content,
    )


def create_container_rail(controls=[], col=1, width=100, height=1000, expand=True, content=None):
    if content:
        content = content
    else:
        content = Column(controls=controls, scroll=ScrollMode.AUTO, col=12)
    return Container(
        bgcolor=color_bg_2(),
        alignment=alignment.center,
        expand=expand,
        col=col,
        border_radius=10,
        # border=Border(
        #     top=BorderSide(0.5, color_border_contenedor()),
        #     right=BorderSide(0.5, color_border_contenedor()),
        #     bottom=BorderSide(0.5, color_border_contenedor()),
        #     left=BorderSide(0.5, color_border_contenedor())),
        width=width,
        padding=10,
        height=height,
        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=color_bg_2(),
            offset=Offset(0, 0),
            blur_style=ShadowBlurStyle.SOLID,
        ),
        content=content,
    )


def container_titulo(label_text="Titulo Container", label_size=11):
    return Container(
        content=Column(controls=[Text(label_text, size=label_size,
                       text_align="center", font_family="Tahoma", color=color_texto())]),  # type: ignore
        col=12,
        bgcolor=color_bg(),
        alignment=alignment.center,
        border_radius=10,
        # expand=True,
        padding=5,
        height=30,
        #     border=Border(
        #         top=BorderSide(2, color_border_contenedor()),
        #         right=BorderSide(2, color_border_contenedor()),
        #         bottom=BorderSide(2, color_border_contenedor()),
        #         left=BorderSide(2, color_border_contenedor())),
        #
    )


def create_Container_gnral(offset=Offset(0, 0)):
    return Container(
        expand=True,
        bgcolor=container_color(),
        offset=offset,

        animate_offset=animation_style
    )
