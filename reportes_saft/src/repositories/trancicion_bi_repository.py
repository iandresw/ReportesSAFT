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

    def obtener_tec_anio_inicio(self, ubicacion: int, anio_inicio_periodo: int):
        query = """
                SELECT COUNT(DISTINCT Catastro.ClaveCatastro) AS Total
                FROM  Catastro INNER JOIN
                F_FichaUrb ON Catastro.ClaveCatastro = F_FichaUrb.ClaveCatastro
                WHERE (Catastro.Ubicacion = ?) AND (DATEPART(year, F_FichaUrb.FechaAvaluo) < ?)
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, anio_inicio_periodo))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_tec_anio_fin(self, ubicacion: int, anio_inicio_periodo: int):
        query = """
                SELECT COUNT(DISTINCT Catastro.ClaveCatastro) AS Total
                FROM  Catastro INNER JOIN
                F_FichaUrb ON Catastro.ClaveCatastro = F_FichaUrb.ClaveCatastro
                WHERE (Catastro.Ubicacion = ?) 
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_dec_anio_inicio(self, ubicacion: int, anio_inicio_periodo: int):
        query = """
                SELECT COUNT(DISTINCT Catastro.ClaveCatastro) AS Total
                FROM  Catastro INNER JOIN
                DeclaraBI ON Catastro.ClaveCatastro = DeclaraBI.ClaveCatastro
                WHERE (Catastro.Ubicacion = ?) AND (DATEPART(year, DeclaraBI.FechaDeclaraBI) < ?) AND (Catastro.ClaveCatastro NOT IN
                             (SELECT        ClaveCatastro
                               FROM            F_FichaUrb))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, anio_inicio_periodo))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_dec_anio_fin(self, ubicacion: int, anio_inicio_periodo: int):
        query = """
SELECT COUNT(DISTINCT Catastro.ClaveCatastro) AS Total
FROM  Catastro INNER JOIN
DeclaraBI ON Catastro.ClaveCatastro = DeclaraBI.ClaveCatastro
WHERE (Catastro.Ubicacion = ?) AND (Catastro.ClaveCatastro NOT IN
                             (SELECT        ClaveCatastro
                               FROM            F_FichaUrb))
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (ubicacion, ))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
