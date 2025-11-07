class CuentaIngresoRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_cuentas(self, cta_ingreso):
        query = " SELECT  TOP (1)  CtaIngreso, NombreCtaIngreso, CtaPermOP, CtaRecuperacion, Tipo, RangoR, Categoria, CtaInteres, CtaRecargos FROM CuentaIngreso_A WHERE (CtaIngreso LIKE ?) AND (Anio = DATEPART(year, GETDATE()))"
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ingreso,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_cuentas_ics(self, cta_ingreso):
        query = " SELECT  CtaRecuperacion, CtaInteres, CtaRecargos FROM CuentaIngreso_A WHERE (CtaIngreso LIKE ?)  GROUP BY CtaRecuperacion, CtaInteres, CtaRecargos ORDER BY CtaRecuperacion DESC, CtaInteres, CtaRecargos"
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_ingreso}%',))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_cta_sp(self, cta_ingreso):
        query = " SELECT  CtaRecuperacion, CtaInteres, CtaRecargos FROM CuentaIngreso_A WHERE (CtaIngreso LIKE ?)  GROUP BY CtaRecuperacion, CtaInteres, CtaRecargos ORDER BY CtaRecuperacion DESC, CtaInteres, CtaRecargos"
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_ingreso}%',))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
