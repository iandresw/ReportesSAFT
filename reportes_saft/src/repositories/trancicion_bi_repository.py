class TrancicionBIRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_bi_urbano(self):
        query = """
                SELECT COUNT(ClaveCatastro) AS Total
                FROM Catastro
                WHERE (Ubicacion = 0)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_bi_rural(self):
        query = """
                SELECT COUNT(ClaveCatastro) AS Total
                FROM Catastro
                WHERE (Ubicacion = 1)
                """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_bi_urbano_activos(self, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.ClaveCatastro) AS Total
            FROM AvPgEnc INNER JOIN
            Catastro ON AvPgEnc.ClaveCatastro = Catastro.ClaveCatastro
            WHERE (Catastro.Ubicacion = 0) AND (AvPgEnc.AvPgEstado = 2) AND (AvPgEnc.AvPgTipoImpuesto = 1)
            AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_bi_rural_activos(self, anio: int):
        query = """
            SELECT COUNT(DISTINCT AvPgEnc.ClaveCatastro) AS Total
            FROM AvPgEnc INNER JOIN
            Catastro ON AvPgEnc.ClaveCatastro = Catastro.ClaveCatastro
            WHERE (Catastro.Ubicacion = 1) AND (AvPgEnc.AvPgEstado = 2) AND (AvPgEnc.AvPgTipoImpuesto = 1)
            AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
