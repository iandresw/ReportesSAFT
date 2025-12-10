class PlanesPagoRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_planes_pago(self, identidad: str):
        query = """SELECT  SeqPP, Identidad, FechaInicioPP, NumCuotasPP, ValorCuotaPP, TotalPagadoPP, MontoPP, EstadoPP
                        FROM  PlanPago
                        WHERE (Identidad = ?)
                        ORDER BY FechaInicioPP
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (identidad,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_detalle(self, num_plan_pago: str):
        query = """SELECT PlanPagoDetalle.NumAvPg, AvPgEnc.AvPgEstado, AvPgEnc.AvPgTipoImpuesto, SUM(AvPgDetalle.ValorUnitAvPgDet) AS Monto
                    FROM  PlanPagoDetalle INNER JOIN
                    AvPgEnc ON PlanPagoDetalle.NumAvPg = AvPgEnc.NumAvPg INNER JOIN
                    AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
                    WHERE (PlanPagoDetalle.SeqPP = ?)
                    GROUP BY PlanPagoDetalle.NumAvPg, AvPgEnc.AvPgEstado, AvPgEnc.AvPgTipoImpuesto
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_factura_cuota(self, num_plan_pago: str):
        query = """SELECT PlanPagoFactura.NumAvPg, AvPgEnc.AvPgEstado, SUM(AvPgDetalle.ValorUnitAvPgDet) AS Monto
                        FROM PlanPagoFactura INNER JOIN
                        AvPgEnc ON PlanPagoFactura.NumAvPg = AvPgEnc.NumAvPg INNER JOIN
                        AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
                        WHERE (PlanPagoFactura.SeqPP = ?)
                        GROUP BY PlanPagoFactura.NumAvPg, AvPgEnc.AvPgEstado 
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_plan_pago,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def pagar_factura_en_pp(self, num_factura: str):
        query = """UPDATE AvPgEnc SET AvpgEstado = 2 WHERE NumAvPg = ? and AvPgEstado = 6   """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_factura,))

    def reversar_factura_en_pp(self, num_factura: str):
        query = """UPDATE AvPgEnc SET AvpgEstado = 1 WHERE NumAvPg = ? and AvPgEstado = 6   """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_factura,))

    def anular_cuota_pp(self, num_factura: str):
        query = """UPDATE AvPgEnc SET AvpgEstado = 3 WHERE NumAvPg = ? and AvPgEstado = 2
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_factura,))

    def obtener_detalle_factura(self, num_factura: str):
        query = """SELECT NumAvPg, ValorUnitAvPgDet, ClaveCatastro, CtaIngreso, CantAvPgDet, RefAvPgDet, DescuentoAvPgDet, RecargoAvPgDet, ValorPagadoAvPgDet, VisibleEnTesAvPgDet, ValorXAvPgDet, DesctoTe
                    FROM AvPgDetalle WHERE NumAvPg = ? order by CtaIngreso
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_factura,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_cta(self, tipo_cta: str):
        query = """SELECT  CtaIngreso FROM  CuentaIngreso_A WHERE (Tipo = ?) GROUP BY CtaIngreso ORDER BY CtaIngreso"""
        with self.conexion.cursor() as cur:
            cur.execute(query, (tipo_cta,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
