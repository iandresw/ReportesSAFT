class TrancicionAMBRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_amb_urbano(self, codAldea: str, ctaIngreso: str):
        query = """SELECT        COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM            AvPgEnc INNER JOIN
                    AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                    CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.AvPgEstado <> 3) AND 
                    (CuentaIngreso_A.Tipo <> 3)
                    """

        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_rural(self, codAldea: str, ctaIngreso: str):
        query = """SELECT        COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM            AvPgEnc INNER JOIN
                    AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                    CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND  (AvPgEnc.AvPgEstado <> 3) AND 
                    (CuentaIngreso_A.Tipo <> 3)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_rural_activos(self, codAldea: str, anio: int, ctaIngreso: str):
        query = """SELECT        COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM            AvPgEnc INNER JOIN
                    AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                    CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)  AND 
                    (CuentaIngreso_A.Tipo <> 3)
                    """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_amb_urbano_activos(self, codAldea: str, anio: int, ctaIngreso: str):
        query = """
                    SELECT        COUNT(DISTINCT AvPgEnc.Identidad) AS Total
                    FROM            AvPgEnc INNER JOIN
                    AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                    Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                    CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                    WHERE        (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.AvPgEstado = 2) AND (DATEPART(year, AvPgEnc.FechaVenceAvPg) = ?)  AND 
                    (CuentaIngreso_A.Tipo <> 3)
                         """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            row = cur.fetchone()
            if not row:
                return None
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
# impuestos de extraccion y selectivo detalle

    def obtener_amb_urbano_detalle(self, codAldea: str, ctaIngreso: str):
        query = """
                SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
                FROM AvPgEnc INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.AvPgEstado <> 3) AND (CuentaIngreso_A.Tipo <> 3)
                GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
              """

        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_amb_rural_detalle(self, codAldea: str, ctaIngreso: str):
        query = """
                SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
                FROM AvPgEnc INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.AvPgEstado <> 3) AND (CuentaIngreso_A.Tipo <> 3)
                GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
            
              """

        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea,  f'{ctaIngreso}%',))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_amb_rural_activos_detalle(self, codAldea: str, anio: int, ctaIngreso: str):
        query = """
                SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
                FROM AvPgEnc INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (Contribuyente.CodAldea <> ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.AvPgEstado = 2) AND (CuentaIngreso_A.Tipo <> 3) and YEAR(AvPgEnc.FechaVenceAvPg)  = ?
                GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
            """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]

    def obtener_amb_urbano_activos_detalle(self, codAldea: str, anio: int, ctaIngreso: str):
        query = """SELECT Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
                FROM AvPgEnc INNER JOIN
                AvPgDetalle ON AvPgEnc.NumAvPg = AvPgDetalle.NumAvPg INNER JOIN
                Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad INNER JOIN
                CuentaIngreso_A ON AvPgDetalle.CtaIngreso = CuentaIngreso_A.CtaIngreso AND YEAR(AvPgEnc.FechaVenceAvPg) = CuentaIngreso_A.Anio
                WHERE  (Contribuyente.CodAldea = ?) AND (AvPgDetalle.CtaIngreso LIKE ?) AND (AvPgEnc.AvPgEstado = 2) AND (CuentaIngreso_A.Tipo <> 3) and YEAR(AvPgEnc.FechaVenceAvPg)  = ?
                GROUP BY Contribuyente.Identidad, Contribuyente.Pnombre, Contribuyente.SNombre, Contribuyente.PApellido, Contribuyente.SApellido
             """
        with self.conexion.cursor() as cur:
            cur.execute(query, (codAldea, f'{ctaIngreso}%', anio))
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
