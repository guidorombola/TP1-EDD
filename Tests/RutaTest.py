import unittest

from Ruta import Ruta


class RutaTest(unittest.TestCase):
    def test_crear_ruta_exitosamente(self):
        ruta = Ruta("Buenos Aires", "La Plata", 50, 100)
        self.assertEqual("Buenos Aires", ruta.origen)
        self.assertEqual("La Plata", ruta.destino)
        self.assertEqual(50, ruta.distancia)
        self.assertEqual(100, ruta.tiempo_de_viaje)


if __name__ == '__main__':
    unittest.main()
