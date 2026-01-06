class DataBaseRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def parametroCont(self):
        query = """
            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'Ambiental' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD Ambiental NVARCHAR(255) DEFAULT '' NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'Justicia' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD Justicia NVARCHAR(255) DEFAULT '' NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'UltNumPO' AND Object_ID = OBJECT_ID('ParametroCont'))
            BEGIN
                ALTER TABLE ParametroCont ADD UltNumPO INT DEFAULT 0 NOT NULL;
            END;

            IF NOT EXISTS(SELECT 1 FROM sys.columns 
                          WHERE Name = 'HorarioAlcohol' AND Object_ID = OBJECT_ID('Tra_PermOP'))
            BEGIN
                ALTER TABLE Tra_PermOP ADD HorarioAlcohol INT DEFAULT 0 NOT NULL;
            END;

        """
        try:
            with self.conexion.cursor() as cur:
                cur.execute(query)

            return True
        except Exception as e:
            print("Error en parametroCont:", e)
            return False
