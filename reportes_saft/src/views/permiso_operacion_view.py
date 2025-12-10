import os
import webbrowser
import flet as ft
from models.tra_permop import Tra_PermOpe
from ui.ui_alertas import AlertaGeneral
from ui.modals.venta_alcohol_modal import abril_venta_alcohol_modal
from ui.ui_checkBox import createCheckBox
from ui.ui_colors import color_bg, color_bg_2, color_texto, color_texto_2, color_texto_parrafo
from ui.ui_radio import create_radio
from ui.ui_botones import create_boton
from ui.ui_text import create_texFiel_fijas
from ui.ui_container import create_container
from services.parametro_service import ParametroService
from services.permiso_operacion_services import PermisooperacionServices
from reports.permiso_operacion_report import PermisoOperacionReport
from reports.per_ope_la_esperanza import PerOpeLaEsperanzaReport
from reports.per_ope_concepcion_report import PerOpeConcepcionReport


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
        self.datos_muni_admin = self.parametro_service.obtener_datos_municipalidad_admin()
        self.datos_system = self.parametro_service.obtener_datos_systema()
        self.repo_permiso = PermisooperacionServices(
            self.app, self.datos_system)

        self.chk_firma_justicia = createCheckBox("¿Firma Justicia?")
        self.chk_horario_alcohol = createCheckBox(
            "¿Horario Venta de Alcohol?", on_change=self.is_Horario_venta_alcol)

        self.rd_tipo_solcitud = ft.RadioGroup(disabled=True, content=ft.Row(
            [create_radio(value="Apertura", label_text="Apertura"),
             create_radio(value="Renovacion", label_text="Renovación")],),
        )
        self.rd_firma = ft.RadioGroup(disabled=True, value='0', content=ft.Row(

            [
                create_radio(value="0", label_text="Ninguno"),
                create_radio(value="1", label_text="Firma Justicia Municipal"),
                create_radio(value="2", label_text="Firma Unidad Ambiental")],),
        )
        if self.datos_muni["CodMuni"] == "1001":
            self.firma = ft.Row([self.rd_firma, self.chk_horario_alcohol])
        else:
            self.firma = self.chk_firma_justicia

        # ALERTAS
        self.alert_recibo = AlertaGeneral(
            titulo=ft.Text("Permiso de Operación"),
            contenido=ft.Text(
                "¡No se encontro Informacion para el numero de recibo ingresado!"),
            actions=[ft.OutlinedButton("Aceptar", on_click=self.acetar_reg),],)
        # BOTONES
        self.permiso: Tra_PermOpe | None

        self.btn_consulta = create_boton(
            "Consulta", on_click=self.consultar_recibo)
        self.btn_guardar = create_boton(
            "Guardar",
            width=130,
            disabled=True,
            on_click=self.guardar_recibo_po)
        self.btn_imprimir = create_boton(
            "Imprimir",
            width=130,
            disabled=True,
            on_click=self.imprimir_rept_po)
        self.btn_horario = create_boton(
            "Horario Venta de Alcohol",
            width=130,
            disabled=False,
            on_click=self.abrir_modal_venta_bebida)
        self.btn_editar = create_boton("Editar", width=130, disabled=True)
        # CAJAS DE TEXTO
        self.txt_no_recibo = create_texFiel_fijas(
            'No. de Recibo', width=95, read_only=False)
        self.txt_no_permiso = create_texFiel_fijas('No. de Permiso')
        self.txt_periodo = create_texFiel_fijas('Periodo',)
        self.txt_ini_operaion = create_texFiel_fijas('Inicio Operacion')
        self.txt_telefono = create_texFiel_fijas('Telefono')
        self.txt_num_renovacion = create_texFiel_fijas('Numero de Renovacion')
        self.txt_rtn = create_texFiel_fijas('R.T.N')
        self.txt_rtm = create_texFiel_fijas('R.T.M.')
        self.txt_fecha_emission = create_texFiel_fijas('Fecha Emision')
        self.txt_nombre_establecimiento = create_texFiel_fijas(
            'Nombre del Establecimiento')
        self.txt_nombrePropietario = create_texFiel_fijas(
            'Nombre del Propietario')
        self.txt_identidad = create_texFiel_fijas('Identidad del Propietario')
        self.txt_ubicacion = create_texFiel_fijas('Direccion')
        self.txt_claveCatastral = create_texFiel_fijas('Clave Catastral')
        self.txt_act_economica = create_texFiel_fijas('Actividad Economica')
        self.txt_tipo_establecimiento = create_texFiel_fijas(
            'Tipo Establecimiento')

        self.conten_acerca_de = create_container(
            expand=True,
            col=12,
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
                              self.txt_telefono,
                              self.txt_num_renovacion
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
                    controls=[
                        self.firma,
                        ft.Divider(),
                        self.rd_tipo_solcitud,
                    ],
                ),
                ft.Divider(),
                ft.Row(
                    alignment=self.ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[self.btn_guardar, self.btn_horario, self.btn_imprimir
                              ],
                ),
            ],
        )
        self.frame = ft.Container(
            expand=True,
            content=ft.ResponsiveRow(
                expand=True,
                controls=[
                    self.conten_acerca_de,
                ],
                alignment=ft.MainAxisAlignment.CENTER, col=12
            )
        )

    def build(self):
        return ft.Column(expand=True, controls=[
            self.frame
        ])

    def is_Horario_venta_alcol(self, e):
        if e.target.value:
            self.btn_horario.disabled = False
        else:
            self.btn_horario.disabled = True

    def abrir_modal_venta_bebida(self, e):
        self.dialog = abril_venta_alcohol_modal(self)
        self.page.open(self.dialog)
        self.page.update()

    def acetar_reg(self, e):
        self.alert_recibo.open = False
        self.alert_recibo.update()

    def consultar_recibo(self, e):
        num_recibo = self.txt_no_recibo.value
        existe = self.repo_permiso.existe_po(num_recibo)
        justicia = self.chk_firma_justicia.value
        tipo_per = self.rd_tipo_solcitud.value
        self.permiso = self.repo_permiso.crear_permiso_operacion(
            int(num_recibo), justicia, tipo_per)  # type: ignore
        if not self.permiso:
            self.page.open(self.alert_recibo)
            return None
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
        self.txt_tipo_establecimiento.value = self.permiso.CodProfesion
        self.rd_tipo_solcitud.value = self.permiso.Observacion
        self.txt_num_renovacion.value = self.permiso.NumeroRenovacion
        self.rd_tipo_solcitud.update()

        if not existe:
            self.btn_guardar.disabled = False
            self.btn_guardar.style.bgcolor = self.bg_color
            self.btn_guardar.update()
            self.btn_imprimir.style.bgcolor = self.bg_2_color
            self.btn_imprimir.disabled = True
            self.btn_imprimir.update()
            self.rd_firma.disabled = False
            self.rd_firma.update()
            self.rd_tipo_solcitud.update()

        else:
            self.btn_guardar.disabled = True
            self.btn_guardar.update()
            self.btn_guardar.style.bgcolor = self.bg_2_color
            self.btn_imprimir.disabled = False
            self.btn_imprimir.style.bgcolor = self.bg_color
            self.btn_imprimir.update()
            if self.datos_muni["CodMuni"] == "1001":
                self.firma.value = str(self.permiso.FirmaJ)

            else:
                self.firma.value = bool(self.permiso.FirmaJ)
            self.firma.disabled = True
            self.firma.update()
        self.page.update()

    def guardar_recibo_po(self, e):
        self.permiso.FirmaJ = self.rd_firma.value
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
            justicia = self.rd_firma.value
            horario_alcoho = self.chk_horario_alcohol.value
            if self.datos_muni["CodMuni"] == "1001":
                reporte = PerOpeLaEsperanzaReport(
                    self.permiso, self.datos_muni, "", justicia, self.datos_muni_admin, horario_alcohol=horario_alcoho)  # type: ignore
            elif self.datos_muni["CodMuni"] == "1403":
                reporte = PerOpeConcepcionReport(
                    self.permiso, self.datos_muni, "", justicia, self.datos_muni_admin)  # type: ignore
            else:
                reporte = PermisoOperacionReport(
                    self.permiso, self.datos_muni, "", justicia)
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
            self.btn_guardar.disabled = True
            self.btn_guardar.style.bgcolor = self.bg_2_color
            self.btn_guardar.update()

            self.btn_imprimir.disabled = True
            self.btn_imprimir.style.bgcolor = self.bg_2_color
            self.btn_imprimir.update()
            self.txt_no_permiso.value = str(self.permiso.NoPermiso)

            self.txt_no_recibo.value = ""
            self.txt_periodo.value = ""
            self.txt_ini_operaion.value = ""
            self.txt_telefono.value = ""
            self.txt_rtm.value = ""
            self.txt_rtn.value = ""
            self.txt_fecha_emission.value = ""
            self.txt_nombre_establecimiento.value = ""
            self.txt_identidad.value = ""
            self.txt_nombrePropietario.value = ""
            self.txt_claveCatastral.value = ""
            self.txt_ubicacion.value = ""
            self.txt_act_economica.value = ""
            self.txt_tipo_establecimiento.value = ""
            self.rd_tipo_solcitud.value = ""
            self.txt_num_renovacion.value = ""
            self.txt_no_permiso.value = ""
            if self.datos_muni["CodMuni"] == "1001":
                self.firma.value = "0"
            else:
                self.firma.value = False

            self.page.update()

        except Exception as ex:
            self.page.open(self.ft.SnackBar(
                ft.Text(f"Error: {str(ex)}", size=14),
                bgcolor=ft.Colors.RED_700,
            ))
            self.btn_guardar.disabled = True
            self.btn_guardar.style.bgcolor = self.bg_color
            self.btn_guardar.update()

            self.btn_imprimir.disabled = True
            self.btn_imprimir.style.bgcolor = self.bg_color
            self.btn_imprimir.update()
            self.page.update()

    def cerrar_modal(self):
        self.dialog.open = False
        self.page.update()
