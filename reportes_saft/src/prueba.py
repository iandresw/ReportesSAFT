
import flet as ft
from flet import Dropdown, dropdown, TextStyle, ButtonStyle
from ui.ui_colors import color_check, color_texto, color_bg_2


def dropbox_aldeas(aldeas: list[dict]):
    aldeas_ordenadas = sorted(aldeas, key=lambda a: a["NombreAldea"])
    return Dropdown(
        label="Seleccione la aldea",
        width=300,
        options=[dropdown.Option(
            key=str(a["CodAldea"]),
            text=a["NombreAldea"],
            text_style=TextStyle(
                size=10, font_family="Tahoma", color=color_texto()),
            style=ButtonStyle(color=color_texto(), text_style=TextStyle(
                size=10, font_family="Tahoma", color=color_texto())))
            for a in aldeas],
        color=color_texto(),
        bgcolor=color_bg_2(),
        label_style=TextStyle(
            size=10, font_family="Tahoma", color=color_texto()),
        text_style=TextStyle(size=10, font_family="Tahoma", color=color_texto()))


def main(page: ft.Page):
    page.title = "Login SAFT"
    aldeas = [{'CodAldea': '042101', 'NombreAldea': 'CASCO URBANO (SANTA RITA)', 'UbicacionAldea': 0},
              {'CodAldea': '042102', 'NombreAldea': 'COPAN RUINAS', 'UbicacionAldea': 0},
              {'CodAldea': '042103', 'NombreAldea': 'BUENA VISTA', 'UbicacionAldea': 0},
              {'CodAldea': '042104', 'NombreAldea': 'DEBAJIADOS ', 'UbicacionAldea': 0},
              {'CodAldea': '042105', 'NombreAldea': 'EL BARRIAL  ', 'UbicacionAldea': 0},
              {'CodAldea': '042106', 'NombreAldea': 'EL CAMPAMENTO ',
                  'UbicacionAldea': 0},
              {'CodAldea': '042107', 'NombreAldea': 'EL CARRIZAL', 'UbicacionAldea': 0},
              {'CodAldea': '042108', 'NombreAldea': 'EL CONAL', 'UbicacionAldea': 0}]
    fropBox = dropbox_aldeas(aldeas)
    page.add(fropBox)


if __name__ == "__main__":
    ft.app(target=main)
