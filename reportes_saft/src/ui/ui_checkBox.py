from flet import Checkbox, TextStyle
from ui.ui_colors import color_check, color_fill_chek, color_texto


def createCheckBox(label_text="", on_change=None):
    return Checkbox(
        fill_color=color_fill_chek(),
        check_color=color_check(),
        label=label_text,
        value=False,
        disabled=False,
        col=12,
        visible=True,
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=color_texto()),
        on_change=on_change,)
