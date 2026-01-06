class PrescripcionesRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtenter_analis_prescripcion(self,  tipo_impuesto: int):
        query = """
            DECLARE @FechaLimite DATE = DATEADD(YEAR, -5, CAST(GETDATE() AS DATE));
            SELECT e.Identidad, Contribuyente.Pnombre + ' ' + Contribuyente.SNombre + ' ' + Contribuyente.PApellido + ' ' + Contribuyente.SApellido AS Nombre, '2020-12-16' AS Expr1, 
            SUM(CASE WHEN e.FechaVenceAvPg < '20201216' THEN d .ValorUnitAvPgDet ELSE 0 END) AS PRESCRITO, SUM(CASE WHEN e.FechaVenceAvPg >= '20201216' THEN d .ValorUnitAvPgDet ELSE 0 END) AS RECUPERABLE, 
            MIN(e.FechaVenceAvPg) AS FechaInicio, MAX(e.FechaVenceAvPg) AS FechaFinal, SUM(d.ValorUnitAvPgDet) AS SALDO
            FROM AvPgEnc AS e INNER JOIN
            AvPgDetalle AS d ON e.NumAvPg = d.NumAvPg INNER JOIN
            Contribuyente ON e.Identidad = Contribuyente.Identidad
            WHERE (e.AvPgTipoImpuesto = ?)
            GROUP BY e.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (tipo_impuesto,))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [column[0] for column in cur.description]
            return [dict(zip(columns, row)) for row in rows]
