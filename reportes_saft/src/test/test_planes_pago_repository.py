import unittest
from unittest.mock import MagicMock
from reportes_saft.src.repositories.planes_pago_repository import PlanesPagoRepository


class TestPlanesPagoRepository(unittest.TestCase):

    def test_obtener_planes_pago(self):
        # --- Mock de conexión y cursor ---
        mock_conexion = MagicMock()
        mock_cursor = MagicMock()
        mock_conexion.cursor.return_value.__enter__.return_value = mock_cursor

        # --- Datos simulados que devolvería la BD ---
        mock_cursor.fetchall.return_value = [
            (1, "1408195500014", "2024-01-01", 12, 100.0, 300.0, 1200.0, "A")
        ]

        mock_cursor.description = [
            ("SeqPP",), ("Identidad",), ("FechaInicioPP",), ("NumCuotasPP",),
            ("ValorCuotaPP",), ("TotalPagadoPP",), ("MontoPP",), ("EstadoPP",)
        ]

        repo = PlanesPagoRepository(mock_conexion)

        resultado = repo.obtener_planes_pago("1408195500014")

        # ----- Asserts -----
        mock_cursor.execute.assert_called_once()  # se llamó execute
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado), 1)  # una fila
        self.assertEqual(resultado[0]["Identidad"], "1408195500014")
        self.assertEqual(resultado[0]["NumCuotasPP"], 12)
        print(type(resultado))


if __name__ == '__main__':
    unittest.main()
