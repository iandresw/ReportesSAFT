class TrancicionIPRepository:
    def __init__(self, conexion):
        self.conexion = conexion
    # DECLARADO

    def obtener_ip_urbano(self, codAldea: str):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural(self, codAldea: str):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea <> ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural_activos(self, codAldea: str, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea <> ?)  AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_urbano_activos(self, codAldea: str, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea = ?)  AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    # OTRAS TASAS
    def obtener_ip_urbano_ot(self, CodAldea: str,  cta_ip: str):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM  AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
            AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
            WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
            (SELECT AvPgEnc_1.Identidad
            FROM  AvPgEnc AS AvPgEnc_1 INNER JOIN
            Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
            WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
            GROUP BY AvPgEnc_1.Identidad))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural_ot(self, CodAldea: str,  cta_ip: str):
        query = """
          SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM  AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
            AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
            WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
            (SELECT AvPgEnc_1.Identidad
            FROM  AvPgEnc AS AvPgEnc_1 INNER JOIN
            Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
            WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
            GROUP BY AvPgEnc_1.Identidad))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_rural_activos_ot(self, codAldea: str,  cta_ip: str, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM  AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
            AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
            WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
            (SELECT AvPgEnc_1.Identidad
            FROM  AvPgEnc AS AvPgEnc_1 INNER JOIN
            Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
            WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
            GROUP BY AvPgEnc_1.Identidad)) AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ip_urbano_activos_ot(self, codAldea: str,  cta_ip: str, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM  AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
            AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
            WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
            (SELECT AvPgEnc_1.Identidad
            FROM  AvPgEnc AS AvPgEnc_1 INNER JOIN
            Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
            WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
            GROUP BY AvPgEnc_1.Identidad))  AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    # DETALLE DECLRADO
    def obtener_ip_urbano_detalle(self, codAldea: str):
        query = """
            SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
            FROM  AvPgEnc INNER JOIN Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE  (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea = ?)
            GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_detalle(self, codAldea: str):
        query = """
            SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
            FROM  AvPgEnc INNER JOIN Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE  (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea <> ?)
            GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_activos_detalle(self, codAldea: str, anio: int):
        query = """
            SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea <> ?)  AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
            GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_urbano_activos_detalle(self, codAldea: str, anio: int):
        query = """
            SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE (AvPgEnc.AvPgTipoImpuesto = 4) AND (Contribuyente.CodAldea = ?)  AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
            GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    # DETALLE OTRAS TASAS

    def obtener_ip_urbano_ot_detalle(self, CodAldea: str,  cta_ip: str):
        query = """
                SELECT  Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
                FROM AvPgEnc INNER JOIN
                Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
                WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
                (SELECT AvPgEnc_1.Identidad FROM  AvPgEnc AS AvPgEnc_1 INNER JOIN
                Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
                WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
                GROUP BY AvPgEnc_1.Identidad))
                GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_ot_detalle(self, CodAldea: str,  cta_ip: str):
        query = """
                SELECT  Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
                FROM AvPgEnc INNER JOIN
                Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
                WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
                (SELECT AvPgEnc_1.Identidad FROM  AvPgEnc AS AvPgEnc_1 INNER JOIN
                Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
                WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
                GROUP BY AvPgEnc_1.Identidad))
                GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (CodAldea, cta_ip,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_rural_activos_ot_detalle(self, codAldea: str,  cta_ip: str, anio: int):
        query = """
            SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
            AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
            WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
            (SELECT  AvPgEnc_1.Identidad
            FROM AvPgEnc AS AvPgEnc_1 INNER JOIN
            Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
            WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
            GROUP BY AvPgEnc_1.Identidad)) AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
            GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_ip_urbano_activos_ot_detalle(self, codAldea: str,  cta_ip: str, anio: int):
        query = """
              SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
            AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg
            WHERE (AvPgEnc.AvPgTipoImpuesto <> 4) AND (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.Identidad NOT IN
            (SELECT  AvPgEnc_1.Identidad
            FROM AvPgEnc AS AvPgEnc_1 INNER JOIN
            Contribuyente AS Contribuyente_1 ON AvPgEnc_1.Identidad = Contribuyente_1.Identidad
            WHERE (AvPgEnc_1.AvPgTipoImpuesto = 4)
            GROUP BY AvPgEnc_1.Identidad)) AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
            GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido, Contribuyente.UltPeriodoFact
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, cta_ip, anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
