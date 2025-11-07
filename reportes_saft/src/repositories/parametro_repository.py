class ParametroRepository:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_parametros(self):
        query = """
        SELECT TOP (1)
            CodMuni, NombreMuni, Version, NombreDepto, DiaProcesoCT, NumHabitantes,
            TasaTerceraEdad, AnosTerceraEdad, DiaProcesoSP, TasaDescPagoAdela, DiaCierreSP,
            DescMaxSP, DescMaxBI, CalculeFMTop, TipoConcertacion, FU_CalculoPesos,
            FU_PorcAdEsq, CalculeFMParcela, FU_DescSegPiso, FU_DescTercPiso, ModoManejoFactSP,
            BotonBanco, DosDigitos, MapaSURE, ManzaHaz, TipoConcertacionRural, MensualQuin,
            dirfoto, MsgBI, MsgIC, MsgSP, MsgAviso, MsgPReq, MsgSReq, MapaSUREru, Email,
            Telefono, Fax, Corte, CalcSP, MuniJunta, CalcOtrosIR, Fotos, Diagrama, PDFS, Encr, PorContri
        FROM Parametro
        """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))

    def obtener_systemParam(self):
        query = """
        SELECT 
            CtaIngresoIP, CtaIngresoCJ, CtaIngresoPermOp, CtaIngresoDescuento, CtaIngresoVolVenta, CtaEgresoFondoPos, CtaEgresoFondoLen, CtaEgresoMask, CtaIngresoMask, CtaIngresoBiRural, CtaIngresoBiUrb, 
            CtaIngresoMultaOPSinPermiso, CtaIngresoMultaDeclaraTarde, CtaIngresoRecargoImp, CtaIngresoRecargoServ, CtaIngresoIntImp, CtaIngresoIntServ, IBi, IIC, IIP, Sp, FechaAmni, FechaIC, FechaIP, FechaSP, DescAmni, Emer, 
            FechaIEmer, FechaFEmer, MotivoEmer, DescEmerBI, MaskCtaIngreso, MaskCtaOP, MaskCtaRecu, TpoCuenta, Pp, FechaPp, FechaAmniI, FechaIcI, FechaIpI, FechaSpI, FechaPpI, IntRecPp, CtaInteresPP, CtaRecargoPP, 
            PorDescAmni, FinAmni, PorDescAmniPP, DescAmniPP
        FROM  SystemParam
        """
        with self.conexion.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            if not row:
                return None

            columns = [column[0] for column in cur.description]
            return dict(zip(columns, row))
