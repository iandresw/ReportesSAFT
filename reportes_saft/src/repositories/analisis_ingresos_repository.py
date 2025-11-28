class AnalisisIngresosRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def analisis_ingresos_anio_act_anio_ant(self, anio: int):
        anio_inicio = int(anio)-1
        anio_final = int(anio)
        fecha_inicio = f"{anio_inicio}0101"
        fecha_final = f"{anio_final}1231"

        parms = (anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio,
                 anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, anio_inicio, anio_final, fecha_inicio, fecha_final)
        query = f"""
            SELECT 
            substring(Recibodet.CtaIngreso,1,8) as cta,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 1 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS enero_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 1 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS enero_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 2 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS febrero_ant, 
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 2 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS febrero_act, 
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 3 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS marzo_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 3 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS marzo_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 4 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS abril_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 4 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS abril_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 5 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS mayo_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 5 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS mayo_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 6 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS junio_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 6 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS junio_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 7 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS julio_ant, 
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 7 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS julio_act, 
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 8 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS agosto_ant, 
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 8 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS agosto_act, 
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 9 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS septiembre_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 9 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS septiembre_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 10 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS octubre_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 10 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS octubre_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) =11 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS noviembre_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) =11 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS noviembre_act,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 12 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS diciembre_ant,
            SUM(CASE WHEN month(Recibo.FechaRecibo) = 12 and year(Recibo.FechaRecibo) = ? THEN ReciboDet.ValorUnitReciboDet ELSE 0 END) AS diciembre_act
                FROM ReciboDet INNER JOIN Recibo ON ReciboDet.NumRecibo = Recibo.NumRecibo 
                WHERE (Recibo.ReciboAnulado = 'False') AND  (Recibo.FechaRecibo BETWEEN ? AND ?)  
                group by substring(Recibodet.CtaIngreso,1,8)
                order by cta
        """
        with self.conexion.cursor() as cur:
            cur.execute(query, parms)
            rows = cur.fetchall()
            if not rows:
                return None
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, r)) for r in rows]
