class AldeaRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_aldea_urbana(self):
        query = "SELECT  MIN(CodAldea) AS CodAldea FROM Aldea"
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
