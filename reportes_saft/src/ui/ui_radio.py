from flet import Radio, TextStyle
from ui.ui_colors import color_check, color_texto


def create_radio(value='0', label_text="") -> Radio:
    return Radio(value=value,
                 label=label_text,
                 fill_color=color_check(),
                 label_style=TextStyle(
                     size=10, color=color_texto(), font_family="Tahoma")
                 )
