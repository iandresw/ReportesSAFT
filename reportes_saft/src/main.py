import flet as ft
from views.login_view import PantallaLogin
from contexts.app_context import AppContext
import logging
from utils.logger_config import configurar_logger


def main(page: ft.Page):
    page.title = "Login SAFT"
    context = AppContext()
    context.init_services()
    log = configurar_logger(
        nombre_app="saft_app",
        nivel=logging.INFO
    )

    login_view = PantallaLogin(page, context, log)
    page.add(login_view.build())


if __name__ == "__main__":
    ft.app(target=main)
