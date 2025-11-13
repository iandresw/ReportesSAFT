import os
import webbrowser
import flet as ft
from models.tra_permop import Tra_PermOpe
from ui.ui_colors import color_bg, color_bg_2, color_texto, color_texto_2, color_texto_parrafo
from ui.ui_alertas import AlertaGeneral
from ui.ui_botones import create_boton
from ui.ui_text import create_texFiel_fijas
from ui.ui_container import create_container
from services.parametro_service import ParametroService
from services.permiso_operacion_services import PermisooperacionServices
from reports.permiso_operacion_report import PermisoOperacionReport


class VistaPermisoOperacion:
    def __init__(self, page, context):
        self.page = page
        self.app = context
        self.app.init_saft()
        self.ft = ft
        self.bg_color = color_bg()
        self.bg_2_color = color_bg_2()
        self.texto_color = color_texto()
        self.texto_color_2 = color_texto_2()
        self.color_parrafo = color_texto_parrafo()

        self.parametro_service = ParametroService(self.app.conexion_saft)
        self.datos_muni = self.parametro_service.obtener_datos_municipalidad()
        self.datos_system = self.parametro_service.obtener_datos_systema()
        self.repo_permiso = PermisooperacionServices(
            self.app.conexion_saft, self.datos_system)
        # BOTONES
        self.permiso: Tra_PermOpe

        self.btn_consulta = create_boton(
            "Consulta", on_click=self.consultar_recibo)
        self.btn_guardar = create_boton(
            "Guardar", width=130, disabled=True, on_click=self.guardar_recibo_po)
        self.btn_imprimir = create_boton(
            "Imprimir", width=130, disabled=True, on_click=self.imprimir_rept_po)
        self.btn_editar = create_boton("Editar", width=130, disabled=True)
        # CAJAS DE TEXTO
        self.txt_no_recibo = create_texFiel_fijas(
            'No. de Recibo', width=95, read_only=False)
        self.txt_no_permiso = create_texFiel_fijas('No. de Permiso', width=95)
        self.txt_periodo = create_texFiel_fijas('Periodo', width=95)
        self.txt_ini_operaion = create_texFiel_fijas(
            'Inicio Operacion', width=95)
        self.txt_telefono = create_texFiel_fijas('Telefono', width=95)
        self.txt_rtn = create_texFiel_fijas('R.T.N', width=130)
        self.txt_rtm = create_texFiel_fijas('R.T.M.', width=130)
        self.txt_fecha_emission = create_texFiel_fijas(
            'Fecha Emision', width=130)
        self.txt_nombre_establecimiento = create_texFiel_fijas(
            'Nombre del Establecimiento', width=420)
        self.txt_nombrePropietario = create_texFiel_fijas(
            'Nombre del Propietario', width=305)
        self.txt_identidad = create_texFiel_fijas(
            'Identidad del Propietario', width=105)
        self.txt_ubicacion = create_texFiel_fijas('Direccion', width=305)
        self.txt_claveCatastral = create_texFiel_fijas(
            'Clave Catastral', width=105)
        self.txt_act_economica = create_texFiel_fijas(
            'Actividad Economica', width=205)
        self.txt_tipo_establecimiento = create_texFiel_fijas(
            'Tipo Establecimiento', width=205)

        self.conten_acerca_de = create_container(
            expand=True,
            height=580,
            col=12,
            controls=[
                ft.Column(
                    alignment=self.ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=self.ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    controls=[
                        ft.Image(src=r"\assets\saft.png"),
                        ft.Text(
                            "PERMISO DE OPERACION DE NEGOCIOS",
                            size=24,
                            weight=self.ft.FontWeight.BOLD,
                            color=self.texto_color,
                            text_align=self.ft.TextAlign.CENTER,
                        ),
                        ft.Divider(),
                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.txt_no_recibo,
                                      self.btn_consulta
                                      ],
                        ),

                        ft.Divider(),

                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.txt_no_permiso,
                                      self.txt_periodo,
                                      self.txt_ini_operaion,
                                      self.txt_telefono
                                      ],
                        ),


                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.txt_rtm,
                                      self.txt_rtn,
                                      self.txt_fecha_emission,
                                      ],
                        ),


                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.txt_nombre_establecimiento,
                                      ],
                        ),

                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.txt_identidad, self.txt_nombrePropietario
                                      ],
                        ),

                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.txt_claveCatastral, self.txt_ubicacion
                                      ],
                        ),

                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.txt_act_economica, self.txt_tipo_establecimiento
                                      ],
                        ),
                        ft.Divider(),
                        ft.Row(
                            alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[self.btn_guardar, self.btn_editar, self.btn_imprimir
                                      ],
                        ),
                    ],
                )
            ],
        )
        self.frame = ft.Container(
            expand=True,
            content=ft.ResponsiveRow(
                controls=[

                    self.conten_acerca_de,
                ],
                alignment=ft.MainAxisAlignment.CENTER, col=12
            )
        )

    def build(self):
        return ft.Column([
            self.frame
        ])

    def consultar_recibo(self, e):
        num_recibo = self.txt_no_recibo.value
        existe = self.repo_permiso.existe_po(num_recibo)
        self.permiso = self.repo_permiso.crear_permiso_operacion(
            int(num_recibo))
        self.txt_no_permiso.value = str(self.permiso.NoPermiso)
        self.txt_periodo.value = str(self.permiso.Periodo)
        self.txt_ini_operaion.value = self.permiso.FechaNac.strftime(
            "%d/%m/%Y")
        self.txt_telefono.value = self.permiso.Telefono
        self.txt_rtm.value = self.permiso.Identidad
        self.txt_rtn.value = self.permiso.rtn
        self.txt_fecha_emission.value = self.permiso.Fecha.strftime("%d/%m/%Y")
        self.txt_nombre_establecimiento.value = self.permiso.Negocio
        self.txt_identidad.value = self.permiso.idrepresentante
        self.txt_nombrePropietario.value = self.permiso.Propietario
        self.txt_claveCatastral.value = self.permiso.ClaveCatastro
        self.txt_ubicacion.value = self.permiso.Ubicacion
        self.txt_act_economica.value = self.permiso.Actividad
        self.txt_tipo_establecimiento.value = ""
        if not existe:
            self.btn_guardar.disabled = False
            self.btn_guardar.style.bgcolor = self.bg_color
            self.btn_guardar.update()
            self.btn_imprimir.style.bgcolor = self.bg_2_color
            self.btn_imprimir.disabled = True
            self.btn_imprimir.update()

        else:
            self.btn_guardar.disabled = True
            self.btn_guardar.update()
            self.btn_guardar.style.bgcolor = self.bg_2_color
            self.btn_imprimir.disabled = False
            self.btn_imprimir.style.bgcolor = self.bg_color
            self.btn_imprimir.update()
        self.page.update()

    def guardar_recibo_po(self, e):
        if self.repo_permiso.guardar_perm_operacion(self.permiso):
            self.btn_guardar.disabled = True
            self.btn_guardar.style.bgcolor = self.bg_2_color
            self.btn_guardar.update()
            self.btn_imprimir.disabled = False
            self.btn_imprimir.style.bgcolor = self.bg_color
            self.btn_imprimir.update()
            self.page.update()

    def imprimir_rept_po(self, e):
        try:
            reporte = PermisoOperacionReport(self.permiso, self.datos_muni, "")
            nombre_archivo = "po_report.pdf"
            ruta = os.path.join(os.getcwd(), nombre_archivo)

            reporte.generar_pdf(ruta)
            webbrowser.open_new_tab(f"file://{ruta}")
            # Mostrar notificación
            fila_nack_bar = ft.Row([ft.ProgressRing(height=20, width=20), ft.Text(
                f"Reporte generado: {nombre_archivo}", size=14)])
            self.page.open(self.ft.SnackBar(fila_nack_bar,
                                            bgcolor=ft.Colors.GREEN_700, duration=20
                                            ))
            self.btn_guardar.disabled = False
            self.btn_guardar.style.bgcolor = self.bg_color
            self.btn_guardar.update()

            self.btn_imprimir.disabled = False
            self.btn_imprimir.style.bgcolor = self.bg_color
            self.btn_imprimir.update()
            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))
            self.btn_guardar.disabled = False
            self.btn_guardar.style.bgcolor = self.bg_color
            self.btn_guardar.update()

            self.btn_imprimir.disabled = False
            self.btn_imprimir.style.bgcolor = self.bg_color
            self.btn_imprimir.update()
            self.page.update()
