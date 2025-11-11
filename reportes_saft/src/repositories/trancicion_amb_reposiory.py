class TrancicionAMBRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_amb_urbano(self, codAldea: str, ctaIngreso: str):
        query = """SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM AvPgEnc INNER JOIN AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
                    WHERE (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?)
                    """

        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_rural(self, codAldea: str, ctaIngreso: str):
        query = """SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM AvPgEnc INNER JOIN AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
                    WHERE (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_rural_activos(self, codAldea: str, anio: int, ctaIngreso: str):
        query = """SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM AvPgEnc INNER JOIN AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
                    WHERE (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?)
                    AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_urbano_activos(self, codAldea: str, anio: int, ctaIngreso: str):
        query = """SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM AvPgEnc INNER JOIN AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
                    WHERE (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?)
                    AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
