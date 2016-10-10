import unittest

from Formateador import Formateador


class FormateadorTest(unittest.TestCase):
    def test_formateo_tiempo_exitosamente(self):
        tiempo = 3366
        tiempo_formateado = (0, 0, 56)
        self.assertEqual(tiempo_formateado, Formateador.formateo_tiempo(self, tiempo))

    def test_formateo_distancia_exitosamente(self):
        distancia = 58158
        distancia_formateada = 58.158
        self.assertEqual(distancia_formateada, Formateador.formateo_distancia(self, distancia))

    def test_estandarizar_texto(self):
        texto = "Uso tildes, sí, ñandú"
        self.assertEqual("Uso tildes, si, nandu", Formateador.estandarizar_texto(self, texto))


if __name__ == '__main__':
    unittest.main()
