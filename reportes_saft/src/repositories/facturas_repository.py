class FacturasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_mora_bi(self, cta_bi: str):
        query = """
            SELECT SUM(AvPgDetalle.ValorUnitAvPgDet) AS valor
                FROM AvPgEnc INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
                WHERE (AvPgEnc.FechaVenceAvPg < GETDATE()) AND (AvPgEnc.AvPgEstado = 1) AND (AvPgDetalle.CtaIngreso = ?) AND (AvPgEnc.AvPgTipoImpuesto = 1)
            GROUP BY AvPgDetalle.CtaIngreso
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_bi,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_mora_ip(self, cta_ip: str):
        query = """
            SELECT SUM(AvPgDetalle.ValorUnitAvPgDet) AS valor
                FROM AvPgEnc INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
                WHERE (AvPgEnc.FechaVenceAvPg < GETDATE()) AND (AvPgEnc.AvPgEstado = 1) AND (AvPgDetalle.CtaIngreso = ?) 
            GROUP BY AvPgDetalle.CtaIngreso
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ip,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_int_rec_ip(self, cta_ip: str):
        query = """
            SELECT SUM(AvPgDetalle.ValorUnitAvPgDet) AS valor
                FROM AvPgEnc INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
                WHERE (AvPgEnc.FechaVenceAvPg < GETDATE()) AND (AvPgEnc.AvPgEstado = 1) AND (AvPgDetalle.CtaIngreso = ?) AND (AvPgEnc.AvPgTipoImpuesto = 4)
            GROUP BY AvPgDetalle.CtaIngreso
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ip,))
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_mora_ics(self, cta_ics: str):
        query = """
                SELECT AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, SUM(AvPgDetalle.ValorUnitAvPgDet) AS valor
                FROM AvPgDetalle INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, AvPgEnc.FechaEmAvPg)
                WHERE (SUBSTRING(AvPgDetalle.CtaIngreso, 1, 6) = ?) AND (AvPgEnc.AvPgEstado = 1)
                GROUP BY AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_ics,))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados

    def obtener_interes_ics(self, cta_intres_ics: str):
        query = """
                SELECT AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, SUM(AvPgDetalle.ValorUnitAvPgDet) AS valor
                FROM AvPgDetalle INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, AvPgEnc.FechaEmAvPg)
                WHERE (AvPgDetalle.CtaIngreso = ?) AND (AvPgEnc.AvPgEstado = 1)
                GROUP BY AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_intres_ics,))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados

    def obtener_tasas_ics(self, cta_intres_ics: str):
        query = """
                SELECT AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, SUM(AvPgDetalle.ValorUnitAvPgDet) AS valor
                FROM AvPgDetalle INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, AvPgEnc.FechaEmAvPg)
                WHERE (AvPgDetalle.CtaIngreso like ?) AND (AvPgEnc.AvPgEstado = 1)
                GROUP BY AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_intres_ics}%',))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados

    def obtener_mora_sp(self, cta_sp: str):
        query = """
                SELECT AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso, SUM(AvPgDetalle.ValorUnitAvPgDet) AS valor
                FROM AvPgDetalle INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso INNER JOIN
                AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg AND CuentaIngreso_A.Anio = DATEPART(year, AvPgEnc.FechaEmAvPg)
                WHERE (AvPgDetalle.CtaIngreso like ?) AND (AvPgEnc.AvPgEstado = 1)
                GROUP BY AvPgDetalle.CtaIngreso, CuentaIngreso_A.NombreCtaIngreso
                """
        with self.conexion.cursor() as cur:
            cur.execute(query, (f'{cta_sp}%',))
            rows = cur.fetchall()

            if not rows:
                return []

            columns = [column[0] for column in cur.description]

            # ✅ Convertir a lista de diccionarios
            resultados = [dict(zip(columns, row)) for row in rows]

            return resultados
