from repositories.planes_pago_repository import PlanesPagoRepository
from datetime import datetime
from dateutil.relativedelta import relativedelta


class PlanesPagoService:
    def __init__(self, conexion):
        self.repo = PlanesPagoRepository(conexion)

    def planes_de_pago(self, identidad):
        planes = self.repo.obtener_planes_pago(identidad=identidad)
        if not planes:
            raise ValueError(
                f"No se encontraron planes de pago para la identidad {identidad}")
        resultados = []
        for plan in planes:
            fecha_inicio = plan["FechaInicioPP"]
            num_cuotas = plan["NumCuotasPP"]
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                fecha_vencimiento = fecha_inicio + \
                    relativedelta(months=num_cuotas)
                vencio = datetime.now() > fecha_vencimiento
            else:
                fecha_vencimiento = fecha_inicio + \
                    relativedelta(months=num_cuotas)
                vencio = datetime.now() > fecha_vencimiento

            if vencio:
                resultados.append({
                    "SeqPP": plan["SeqPP"],
                    "FechaInicio": fecha_inicio,
                    "Cuotas": num_cuotas,
                    "ValorCuota": plan["ValorCuotaPP"],
                    "TotalPagado": plan["TotalPagadoPP"],
                    "MontoPP": plan["MontoPP"],
                    "FechaVencimiento": fecha_vencimiento,
                    "Vencio": vencio
                })
        print(resultados)
        for plan_vencido in resultados:
            print(plan_vencido["SeqPP"])
            cuotas_pagadas = self.repo.obtener_factura_cuota(
                plan_vencido["SeqPP"])
            if not cuotas_pagadas:
                raise ValueError(
                    f"No se encontraron cuotas para el plan de pago {plan_vencido["SeqPP"]}")
            valor_pagado = 0
            for cuotas_pag in cuotas_pagadas:
                if cuotas_pag["AvPgEstado"] == 2:
                    valor_pagado += cuotas_pag["Monto"]

            facturas_en_pp = self.repo.obtener_detalle(plan_vencido["SeqPP"])

            if not facturas_en_pp:
                raise ValueError(
                    f"No se encontraron cuotas para el plan de pago {plan_vencido["SeqPP"]}")
            valor_factura = 0
            for facturas_pp in facturas_en_pp:
                if facturas_pp["Monto"] < valor_pagado:
                    # self.repo.pagar_factura_en_pp(facturas_pp["NumAvPg"])
                    valor_factura += facturas_pp["Monto"]
                    valor_pagado -= facturas_pp["Monto"]
                    if valor_pagado == 0:
                        return 0
                elif facturas_pp["Monto"] > valor_pagado:
                    if valor_pagado != 0:
                        data_factura = self.repo.obtener_detalle_factura(
                            facturas_pp["NumAvPg"])
                        if not data_factura:
                            raise ValueError(
                                f"No se encontraron cuotas para el plan de pago {plan_vencido["SeqPP"]}")

                        cuentas_interes = {c["CtaIngreso"]
                                           for c in self.repo.obtener_cta('2') or []}
                        cuentas_sp = {c["CtaIngreso"]
                                      for c in self.repo.obtener_cta('3') or []}

                        cuentas_actividad = {c["CtaIngreso"]
                                             for c in self.repo.obtener_cta('0') or []}
                        cuentas_impuesto = {c["CtaIngreso"]
                                            for c in self.repo.obtener_cta('1') or []}
                        fact_abono = []
                        val_abono = 0
                        for fact in data_factura:
                            if fact["CtaIngreso"] in cuentas_interes:
                                if fact["ValorUnitAvPgDet"] < valor_pagado:
                                    fact_abono.append({
                                        "Monto": fact["ValorUnitAvPgDet"],
                                        "cta": fact["CtaIngreso"],
                                        "CantAvPgDet": fact["CantAvPgDet"],
                                    })
                                    val_abono += fact["ValorUnitAvPgDet"]
                                    valor_pagado -= fact["ValorUnitAvPgDet"]
                                    if valor_pagado == 0:
                                        return 0
                            if fact["CtaIngreso"] in cuentas_impuesto or fact["CtaIngreso"] in cuentas_actividad:
                                if fact["ValorUnitAvPgDet"] < valor_pagado:
                                    fact_abono.append({
                                        "Monto": fact["ValorUnitAvPgDet"],
                                        "cta": fact["CtaIngreso"],
                                        "CantAvPgDet": fact["CantAvPgDet"],
                                    })
                                    val_abono += fact["ValorUnitAvPgDet"]
                                    valor_pagado -= fact["ValorUnitAvPgDet"]
                                    if valor_pagado == 0:
                                        return 0
                            if fact["CtaIngreso"] in cuentas_sp:
                                if fact["ValorUnitAvPgDet"] > valor_pagado:

                                    fact_abono.append({
                                        "Monto": valor_pagado,
                                        "cta": fact["CtaIngreso"],
                                        "CantAvPgDet": fact["CantAvPgDet"],
                                    })
                                    val_abono += valor_pagado
                                    valor_pagado -= valor_pagado
                                    if valor_pagado == 0:
                                        return 0
                                else:
                                    val = fact["ValorUnitAvPgDet"] - \
                                        valor_pagado
                                    print(
                                        f"aplico abono {val} {fact["ValorUnitAvPgDet"]} {valor_pagado}")
                                    fact_abono.append({
                                        "Monto": valor_pagado,
                                        "cta": fact["CtaIngreso"],
                                        "CantAvPgDet": fact["CantAvPgDet"],
                                    })
                                    val_abono += valor_pagado
                                    valor_pagado -= valor_pagado
                                    if valor_pagado == 0:
                                        return 0

                else:
                    self.repo.reversar_factura_en_pp("NumAvPg")
