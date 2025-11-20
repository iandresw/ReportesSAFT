import flet as ft
from utils.credenciales import ManejadorCredenciales
from ui.ui_text import text_usuario, text_usuario_password
from ui.ui_colors import color_bg, color_bg_2, color_texto, color_texto_2, color_texto_parrafo
from views.layout_view import UILayout


class PantallaLogin:
    def __init__(self, page: ft.Page, context):
        self.page = page
        self.context = context
        self.usuario_input = text_usuario()
        self.pass_input = text_usuario_password()

        self.msg = ft.Text("", color="red", size=14)
        self.checkbox = ft.Checkbox(
            label="Recordar contraseña", check_color='black', height=23)

        # Configuración ventana
        self.x_width = 720
        self.x_height = 440
        self.color_bg2 = color_bg()
        self.color_bg1 = color_bg_2()

    def configurar_ventana(self):
        self.page.padding = 0
        self.page.bgcolor = ft.Colors.BLACK
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.maximizable = False
        self.page.window.minimizable = False
        self.page.window.resizable = False
        self.page.window.width = self.x_width
        self.page.window.height = self.x_height
        self.page.window.max_height = self.x_height
        self.page.window.min_height = self.x_height
        self.page.window.max_width = self.x_width
        self.page.window.min_width = self.x_width
        self.page.window.center()
        self.page.update()

    def login_clicked(self, e):
        usuario: str = str(self.usuario_input.value)
        contrasena = str(self.pass_input.value)
        if self.context.auth_service.login(usuario, contrasena):
            if self.checkbox.value:
                ManejadorCredenciales.guardar(usuario, contrasena)
            else:
                ManejadorCredenciales.borrar()
            self.msg.value = "Usuario Ingresado"
            self.page.update()
            self.page.clean()

            index = UILayout(self.page, self.context)
            self.page.add(index.build())
        else:
            self.msg.value = "Usuario o contraseña incorrectos"
            self.page.update()

    def construir_formulario(self):
        return ft.Column([
            ft.Container(ft.Text('Inicia Sesión', width=360, size=30, weight=ft.FontWeight.W_900, text_align=ft.TextAlign.CENTER,
                         color=color_texto()), alignment=ft.Alignment(0, 0), padding=ft.Padding(left=0, top=20, right=0, bottom=0)),
            ft.Container(self.usuario_input, padding=ft.Padding(
                left=20, top=10, right=0, bottom=0)),
            ft.Container(self.pass_input, padding=ft.Padding(
                left=20, top=10, right=0, bottom=0)),
            ft.Container(self.checkbox, alignment=ft.Alignment(
                0, 0), padding=ft.Padding(left=0, top=0, right=0, bottom=0)),
            ft.Container(ft.ElevatedButton(content=ft.Text('INICIAR', color='white',
                         weight=ft.FontWeight.W_500), width=280, bgcolor='black', on_click=self.login_clicked,), ),
            ft.Container(self.msg, padding=ft.Padding(
                left=20, top=5, right=0, bottom=0)),
            ft.Row([ft.Container(ft.Image(src='/saft.png', width=50, height=40)), ft.Container(ft.Image(
                src='/Logo_amhon.png', width=100, height=90))], alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def construir_panel_bienvenida(self):
        return ft.Column([
            ft.Text('Bienvenido!', width=360, size=30, weight=ft.FontWeight.W_900,
                    text_align=ft.TextAlign.CENTER, color=color_texto_parrafo()),
            ft.Container(ft.Image(src='/img-login.png', width=300)),
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def build(self):
        # Cargar credenciales guardadas
        cred = ManejadorCredenciales.cargar()
        self.usuario_input.value = cred["usuario"]
        self.pass_input.value = cred["password"]
        self.checkbox.value = cred["usuario"] != ""

        self.configurar_ventana()

        contenido = ft.Container(
            ft.Row([
                ft.Container(self.construir_formulario(),
                             bgcolor=self.color_bg1, expand=True),
                ft.Container(self.construir_panel_bienvenida(), bgcolor=self.color_bg2,
                             expand=True,
                             border_radius=ft.BorderRadius(top_left=70, top_right=0, bottom_left=70, bottom_right=0)),
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            width=700,
            height=400,
            bgcolor=self.color_bg1,
        )

        return contenido
