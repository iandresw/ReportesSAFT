class PermisoOperacionReposirory:
    def __init__(self, conexion) -> None:
        self.conexion = conexion

    def existe_recibo(self, num_recibo: int) -> bool:
        query = "SELECT COUNT(*) as Total FROM Tra_PermOP WHERE NumRecibo = ?"
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return False
            return row[0] > 0

    def recargar_datos(self, num_recibo: int):
        query = """
            SELECT Tra_PermOP.NumRecibo, Tra_PermOP.Identidad, Tra_PermOP.NoPermiso,  Contribuyente.Direccion,  Contribuyente.IdRepresentante, Tra_PermOP.Periodo, Tra_PermOP.Negocio, Tra_PermOP.Propietario,
                Tra_PermOP.Ubicacion, Tra_PermOP.Actividad, Tra_PermOP.Usuario, Tra_PermOP.FirmaJ , Tra_PermOP.UsuarioMod, Contribuyente.CodProfesion, Contribuyente.FechaNac, Contribuyente.ClaveCatastro, Tra_PermOP.Observacion,
                Contribuyente.rtn, Tra_PermOP.CodAldea, Contribuyente.idrepresentante , Contribuyente.Telefono , Tra_PermOP.Fecha
            FROM Tra_PermOP INNER JOIN 
            Contribuyente ON Tra_PermOP.Identidad = Contribuyente.Identidad 
            WHERE  Tra_PermOP.NumRecibo = ?
        
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return []
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_datos(self, num_recibo: int):
        query = """
         SELECT ReciboDet.NumRecibo, AvPgEnc.Identidad, Contribuyente.Direccion, Contribuyente.IdRepresentante, Contribuyente.rtn,
             Contribuyente_1.Pnombre, Contribuyente_1.SNombre, Contribuyente_1.PApellido, Contribuyente_1.SApellido, 
             CuentaIngreso_A.NombreCtaIngreso, Contribuyente.CodProfesion, Contribuyente.FechaNac, Contribuyente.Pnombre AS Negocio, Contribuyente.ClaveCatastro , Contribuyente.Telefono , Contribuyente.UltPeriodoFact, Contribuyente.CodAldea
             FROM AvPgEnc INNER JOIN ReciboDet ON AvPgEnc.NumAvPg = ReciboDet.NumFactura 
             INNER JOIN Contribuyente ON AvPgEnc.Identidad = Contribuyente.Identidad 
             INNER JOIN Contribuyente AS Contribuyente_1 ON Contribuyente.IdRepresentante = Contribuyente_1.Identidad 
             INNER JOIN CuentaIngreso_A ON Contribuyente.CodProfesion = CuentaIngreso_A.CtaIngreso 
             WHERE (ReciboDet.NumRecibo = ?) AND (AvPgEnc.AvPgTipoImpuesto in( 2,3,7))
             GROUP BY ReciboDet.NumRecibo, AvPgEnc.Identidad, Contribuyente.Direccion, Contribuyente.IdRepresentante, Contribuyente.rtn, 
             Contribuyente_1.Pnombre, Contribuyente_1.SNombre, Contribuyente_1.PApellido, Contribuyente_1.SApellido, 
             CuentaIngreso_A.NombreCtaIngreso, Contribuyente.CodProfesion, Contribuyente.FechaNac, Contribuyente.Pnombre, Contribuyente.ClaveCatastro, Contribuyente.Telefono, Contribuyente.UltPeriodoFact, Contribuyente.CodAldea 

        """
        with self.conexion.cursor() as cur:
            cur.execute(query, (num_recibo,))
            row = cur.fetchone()
            if not row:
                return []
            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_num_po(self,):
        query1 = f"""SELECT UltNumPO FROM ParametroCont;
        """
        query2 = f"""SELECT COUNT(NoPermiso) AS UltNumPO FROM Tra_PermOP"""
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query1)
                row = cur.fetchone()
                if not row:
                    return []
                columns = [column[0] for column in cur.description]
                self.update_ult_po(columns[0]+1)
                return dict(zip(columns, row))
        except Exception as e:
            print(f"Error Consultar ParametroCont: {e}")
            try:
                with self.conexion.cursor() as cur:
                    cur.execute(query2)
                    row = cur.fetchone()
                    if not row:
                        return []
                    columns = [column[0] for column in cur.description]
                    return dict(zip(columns, row))
            except Exception as e2:
                print(f"Error Consultar Tra_PermOP {e2}")
                return []  # En caso de fallo total, datos vacíos

    def update_ult_po(self, ult_num_po: int) -> bool:
        query = "UPDATE ParametroCont SET  UltNumPO = ?"
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query, (ult_num_po,))
                return True
        except Exception as e:
            return False

    def insertar_tra_perm_ope(self, NoPermiso, Periodo, Identidad, Negocio, Propietario, Ubicacion, Actividad,  Observacion,  Fecha, CodAldea, NumRecibo, FirmaJ):
        query = """INSERT INTO Tra_PermOP (NoPermiso, Periodo, Identidad, Negocio, Propietario, Ubicacion, Actividad,  Observacion,  Fecha, CodAldea, NumRecibo, FirmaJ) 
        VALUES (?, ?, ?, ?, ?, ?, ?,  ?,  ?, ?, ?, ?) """
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query, (NoPermiso, Periodo, Identidad, Negocio, Propietario,
                            Ubicacion, Actividad,  Observacion,  Fecha, CodAldea, NumRecibo, FirmaJ))
                return True
        except Exception as e:
            return False
