
# ui/reportes/botones_reportes.py
from ui.ui_cards import metric_card
import flet as ft


def metric_cards(vista):
    valores = vista.data_card
    total_generado = f"{valores[0]["TotalGenerado"]:,.0f}"
    total_facturas_pagadas = f"{valores[0]["IngresosTotalFacturas"]:,.0f}"
    total_facturas = f"{valores[0]["TotalFacturas"]:,.0f}"
    total_facturas_mora = f"{valores[0]["MoraTotalFacturas"]:,.0f}"
    porcentaje_mora = f"{valores[0]["PorcentajeMora"]:,.2f}"
    total_mora = f"{valores[0]["MoraTotal"]:,.2f}"
    ingresos = f"{valores[0]["Ingresos"]:,.2f}"
    num = f"{valores[0]["TotalGenerado"]:,.2f}"

    return [
        metric_card("Total Generado", total_generado),
        metric_card("Total Facturas", total_facturas),
        metric_card("Total Mora", total_mora, "#D32F2F"),
        metric_card("Facturas en Mora", total_facturas_mora, "#D32F2F"),
        metric_card("Monto Recaudado", ingresos, "#388E3C"),
        metric_card("Facturas Pagadas", total_facturas_pagadas, "#388E3C"),
        metric_card("Porcentaje Mora", porcentaje_mora, "#F57C00"),
    ]


def grafico_mora_por_anio(vista):
    valores = vista.data_grafico
    anios = [d["anio"] for d in valores]
    porc_mora = [f"{(d.get('PorcentajeMora') or 0):,.2f}" for d in valores]
    porc_ingresos = [
        f"{(d.get('PorcentajeIngresos') or 0):,.2f}" for d in valores]

    # Convertimos listas a barras
    barras_mora = [
        ft.BarChartRod(
            from_y=0,
            to_y=float(porc_mora[i]),
            color=ft.Colors.RED,     # puedes cambiar
            tooltip=f"{porc_mora[i]}%"
        )
        for i in range(len(porc_mora))
    ]

    barras_ing = [
        ft.BarChartRod(
            from_y=0,
            to_y=float(porc_ingresos[i]),
            color=ft.Colors.GREEN,   # puedes cambiar
            tooltip=f"{porc_ingresos[i]}%"
        )
        for i in range(len(porc_ingresos))
    ]

    return ft.BarChart(
        expand=True,
        max_y=100,
        bar_groups=[
            ft.BarChartGroup(
                x=i,
                bar_rods=[barras_mora[i], barras_ing[i]],
            )
            for i in range(len(anios))
        ],


        border=ft.Border(
            bottom=ft.BorderSide(2, ft.Colors.BLACK),
            left=ft.BorderSide(2, ft.Colors.BLACK)
        ),
        left_axis=ft.ChartAxis(
            title=ft.Text("Porcentaje (%)"),
            title_size=12
        ),
        bottom_axis=ft.ChartAxis(
            title=ft.Text("Año"),
            title_size=12,
            labels=[
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Text(anios[i], size=11)
                )
                for i in range(len(anios))
            ]


        ),
        interactive=True,
        animate=1_000,
    )
