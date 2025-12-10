class DashboardRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_valores_cards(self):
        query = """
            SELECT 
            SUM(AvPgDetalle.ValorUnitAvPgDet) AS TotalGenerado,
            COUNT(AvPgDetalle.NumAvPg) as TotalFacturas,
            SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN 1 ELSE 0 END) AS MoraTotalFacturas, 
            SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS MoraTotal, 
            SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN 1 ELSE 0 END) AS IngresosTotalFacturas, 
            SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS Ingresos,  
            CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) END AS PorcentajeMora,
            CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) END AS PorcentajeIngresos

            FROM AvPgDetalle INNER JOIN AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg 
            WHERE (AvPgEnc.AvPgEstado in (1,2)) AND  (AvPgEnc.FechaVenceAvPg < GETDATE())  
        """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_valores_grafico(self):
        query = """
            SELECT 
            year(AvPgEnc.FechaVenceAvPg) as anio,
            CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) END AS PorcentajeMora,
            CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) END AS PorcentajeIngresos
            FROM AvPgDetalle INNER JOIN AvPgEnc ON AvPgDetalle.NumAvPg = AvPgEnc.NumAvPg 
            WHERE (AvPgEnc.AvPgEstado in (1,2)) AND  (AvPgEnc.FechaVenceAvPg < GETDATE())  
            group by year(AvPgEnc.FechaVenceAvPg)
            order by anio

        """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            if not rows:
                return None

            columns = [column[0] for column in cur.description]

            return [dict(zip(columns, row)) for row in rows]
