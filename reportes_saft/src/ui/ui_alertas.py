from flet import AlertDialog, Text, MainAxisAlignment


def AlertaGeneral(actions=[], titulo=Text("Alerta"), contenido=Text("¿Esta seguro de terminar de ingresar cuentas?")):
    return AlertDialog(
        modal=True,
        title=titulo,
        content=contenido,
        actions=actions,
        actions_alignment=MainAxisAlignment.END,
        )
