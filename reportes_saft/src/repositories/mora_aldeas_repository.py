class MoraAldeasRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def mora_vs_ingresos_general(self, tipo_impuesto='0,1,2,3,4,5,7'):

        lista_tipo = [x.strip() for x in tipo_impuesto.split(",")]

        placeholders = ",".join(["?"] * len(lista_tipo))

        query = f"""
        SELECT Contribuyente.CodAldea, 
        Aldea.NombreAldea, 
        SUM(AvPgDetalle.ValorUnitAvPgDet) AS TotalGenerado,
        COUNT(AvPgDetalle.NumAvPg) as totalFacturas,
        SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN 1 ELSE 0 END) AS MoraTotalFacturas, 
        SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS MoraTotal, 
        SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN 1 ELSE 0 END) AS ingresosTotalFacturas, 
        SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS Ingresos,  
        CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) END AS PorcentajeMora,
        CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) END AS PorcentajeIngresos
        FROM AvPgEnc INNER JOIN
        AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
        Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
        Aldea ON Contribuyente.CodAldea = Aldea.CodAldea
        WHERE (AvPgEnc.AvPgEstado IN (1, 2)) and (AvPgEnc.AvPgTipoImpuesto IN ({placeholders})) and ( AvPgEnc.FechaVenceAvPg < getdate())
        GROUP BY Contribuyente.CodAldea, Aldea.NombreAldea
        ORDER BY PorcentajeMora
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (lista_tipo))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def mora_bi_ubicacion(self, cod_aldea: str, ubicacion: int):

        query = f"""
            SELECT YEAR(AvPgEnc.FechaVenceAvPg) AS anio, Catastro.CodAldea, Aldea.NombreAldea, SUM(AvPgDetalle.ValorUnitAvPgDet) AS TotalGenerado, COUNT(AvPgDetalle.NumAvPg) AS totalFacturas, 
            SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN 1 ELSE 0 END) AS MoraTotalFacturas, SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS MoraTotal, 
            SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN 1 ELSE 0 END) AS ingresosTotalFacturas, SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet ELSE 0 END) AS Ingresos, 
            CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 1 THEN AvPgDetalle.ValorUnitAvpgDet END) * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) 
            END AS PorcentajeMora, CASE WHEN SUM(AvPgDetalle.ValorUnitAvpgDet) = 0 THEN 0 ELSE ROUND(SUM(CASE WHEN AvPgEnc.AvPgEstado = 2 THEN AvPgDetalle.ValorUnitAvpgDet END) 
            * 100.0 / SUM(AvPgDetalle.ValorUnitAvpgDet), 2) END AS PorcentajeIngresos
            FROM Catastro INNER JOIN
            Aldea ON Catastro.CodAldea = Aldea.CodAldea INNER JOIN
            AvPgEnc INNER JOIN
            AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg ON Catastro.ClaveCatastro = AvPgEnc.ClaveCatastro
            WHERE (AvPgEnc.AvPgEstado IN (1, 2)) AND (AvPgEnc.AvPgTipoImpuesto = 1) AND (AvPgEnc.FechaVenceAvPg < GETDATE()) AND (Catastro.CodAldea = ?) AND (Catastro.Ubicacion = ?)
            GROUP BY YEAR(AvPgEnc.FechaVenceAvPg), Catastro.CodAldea, Aldea.NombreAldea
            ORDER BY anio
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (cod_aldea, ubicacion))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
