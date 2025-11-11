class TrancicionSPRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_sp_gob_inicio(self, cta_sp: str, anio: int):
        query = """
            SELECT SUBSTRING(AvPgDetalle.CtaIngreso, 1, 8) AS Cuenta, COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgDetalle INNER JOIN
            AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg
            WHERE (SUBSTRING(AvPgDetalle.CtaIngreso, 1, 6) IN (?)) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) < ?)
            GROUP BY SUBSTRING(AvPgDetalle.CtaIngreso, 1, 8)
            ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp, anio,))
            rows = cur.fetchall()
            if not rows:
                return []
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_sami_inicio(self, anio: int, cta_sp: str):
        query = """
                SELECT SUBSTRING(AvPgDetalle.CtaIngreso, 1, 9) AS Cuenta, COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                FROM AvPgDetalle INNER JOIN
                AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg
                WHERE (DATEPART(year, AvPgEnc.FechaVenceAvPg) > ?) AND (SUBSTRING(AvPgDetalle.CtaIngreso, 1, 7) IN (?))
                GROUP BY SUBSTRING(AvPgDetalle.CtaIngreso, 1, 9)
                ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (anio, cta_sp))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_gob_final(self, cta_sp: str):
        query = """
            SELECT SUBSTRING(AvPgDetalle.CtaIngreso, 1, 8) AS Cuenta, COUNT(DISTINCT AvPgEnc.Identidad) AS Total
            FROM AvPgDetalle INNER JOIN
            AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg
            WHERE (SUBSTRING(AvPgDetalle.CtaIngreso, 1, 6) IN (?)) 
            GROUP BY SUBSTRING(AvPgDetalle.CtaIngreso, 1, 8)
            ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]

    def obtener_sp_sami_final(self, cta_sp: str):
        query = """
                SELECT SUBSTRING(AvPgDetalle.CtaIngreso, 1, 9) AS Cuenta, COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                FROM AvPgDetalle INNER JOIN
                AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg
                WHERE  (SUBSTRING(AvPgDetalle.CtaIngreso, 1, 7) IN (?))
                GROUP BY SUBSTRING(AvPgDetalle.CtaIngreso, 1, 9)
                ORDER BY Cuenta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cta_sp,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
