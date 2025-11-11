class TrancicionICSRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_ics_urbano(self, codAldea: str):
        query = """
            SELECT COUNT(Identidad) AS Total FROM Contribuyente WHERE (Tipo = 1) AND (CodAldea = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ics_rural(self, codAldea: str):
        query = """
           SELECT COUNT(Identidad) AS Total FROM Contribuyente WHERE (Tipo = 1) AND (CodAldea <> ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_isc_rural_activos(self, codAldea: str, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE  (Contribuyente.Tipo = 1) and (Contribuyente.CodAldea <> ?)  AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_ics_urbano_activos(self, codAldea: str, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgEnc INNER JOIN
            Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad
            WHERE   (Contribuyente.Tipo = 1)  AND (Contribuyente.CodAldea = ?)  AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
