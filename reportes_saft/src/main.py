import flet as ft
from views.login_view import PantallaLogin
from contexts.app_context import AppContext


def main(page: ft.Page):
    page.title = "Login SAFT"
    context = AppContext()
    context.init_services()
    login_view = PantallaLogin(page, context)
    page.add(login_view.build())


if __name__ == "__main__":
    ft.app(target=main)
