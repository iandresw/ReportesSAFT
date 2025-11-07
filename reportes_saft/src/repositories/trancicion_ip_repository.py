class TrancicionIPRepository:
    def __init__(self, conexion):
        self.conexion = conexion

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
