import flet as ft
import threading
from updater.updater import iniciar_descarga_actualizacion


def main(page: ft.Page):
    page.title = "Actualizando Reportes SAFT"
    page.window_width = 420
    page.window_height = 240
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    texto_estado = ft.Text("Preparando actualización...", size=14)
    barra = ft.ProgressBar(width=320, value=0)
    porcentaje = ft.Text("0%", size=12)
    boton = ft.ElevatedButton(
        "Cancelar", on_click=lambda e: page.window_destroy())

    page.add(
        ft.Column(
            [
                ft.Text("🔄 Actualizando aplicación", size=20, weight="bold"),
                texto_estado,
                barra,
                porcentaje,
                boton,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    def progreso_callback(value, total):
        if total > 0:
            barra.value = value / total
            porcentaje.value = f"{int(value * 100 / total)}%"
            page.update()

    def estado_callback(msg):
        texto_estado.value = msg
        page.update()

    def tarea_actualizacion():
        ok = iniciar_descarga_actualizacion(progreso_callback, estado_callback)
        if ok:
            estado_callback("✅ Actualización completada. Reiniciando...")
            page.update()
        else:
            estado_callback("❌ Error durante la actualización.")
            page.update()

    hilo = threading.Thread(target=tarea_actualizacion)
    hilo.start()


ft.app(target=main)
