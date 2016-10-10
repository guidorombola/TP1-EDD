import unittest

from Excepciones import *
from MotorDeTrayectos import MotorDeTrayectos
from Trayecto import Trayecto
from time import sleep

class MotorDeTrayectosTest(unittest.TestCase):

    def setUp(self):
        self.motor = MotorDeTrayectos()
        sleep(1)

    def tearDown(self):
        self.motor = None

    def test_crear_trayecto_exitosamente(self):
        self.motor.crear_trayecto("Ejemplo", "Buenos Aires", "Tandil")
        self.assertTrue("Ejemplo" in self.motor.diccionario_de_trayectos)

    def test_crear_trayecto_NombreVacioError(self):
        with self.assertRaises(NombreVacioError):
            self.motor.crear_trayecto("", "Buenos Aires", "Bogota")

    def test_crear_trayecto_NoExisteCaminoError(self):
        with self.assertRaises(NoExisteCaminoError):
            self.motor.crear_trayecto("Ejemplo", "Buenos Aires", "Hong Kong")

    def test_agregar_ciudad_al_final_exitosamente(self):
        self.motor.crear_trayecto("Ejemplo", "Buenos Aires", "Tandil")
        self.motor.agregar_ciudad_al_final("Ejemplo", "Mar del Plata")
        trayecto = self.motor.diccionario_de_trayectos["Ejemplo"].lista_de_rutas
        self.assertEqual("Mar del Plata, Buenos Aires, Argentina", trayecto[-1].destino)

    def test_agregar_ciudad_al_final_NoExisteTrayectoError(self):
        self.motor.crear_trayecto("Ejemplo", "Buenos Aires", "Tandil")
        with self.assertRaises(NoExisteTrayectoError):
            self.motor.agregar_ciudad_al_final("Ejempito", "Tandil")

    def test_agregar_ciudad_exitosamente(self):
        self.motor.crear_trayecto("Ejemplo", "Buenos Aires", "Tandil")
        self.motor.agregar_ciudad("Ejemplo", "Tandil", "Mar del Plata")
        trayecto = self.motor.diccionario_de_trayectos["Ejemplo"].lista_de_rutas
        self.assertEqual("Mar del Plata, Buenos Aires, Argentina", trayecto[0].destino)
        self.assertEqual("Mar del Plata, Buenos Aires, Argentina", trayecto[1].origen)

    def test_agregar_ciudad_NoExisteTrayectoError(self):
        self.motor.crear_trayecto("Ejemplo", "Buenos Aires", "Tandil")
        with self.assertRaises(NoExisteTrayectoError):
            self.motor.agregar_ciudad("Ejemplito", "Tandil", "Mar del Plata")

    def test_concatenar_trayectos(self):
        self.motor.crear_trayecto("Primero", "Rosario", "Parana")
        self.motor.crear_trayecto("Segundo", "La Pampa", "Mendoza")
        self.motor.concatenar_trayectos("Primero", "Segundo", "Concatenado")
        self.assertTrue("Concatenado" in self.motor.diccionario_de_trayectos)
        trayecto_concatenado_esperado = Trayecto(self, "Rosario", "Parana")
        trayecto_concatenado_esperado.agregar_ciudad_al_final("La Pampa")
        trayecto_concatenado_esperado.agregar_ciudad_al_final("Mendoza")
        self.assertListEqual(trayecto_concatenado_esperado.lista_de_rutas,
                             self.motor.diccionario_de_trayectos["Concatenado"].lista_de_rutas)

    def test_concatenar_trayectos_NoExisteTrayectoError(self):
        self.motor.crear_trayecto("Ejemplo", "Rawson, Chubut", "Salta")
        self.motor.crear_trayecto("Ejemplo1", "Bahia Blanca", "Cordoba")
        with self.assertRaises(NoExisteTrayectoError):
            self.motor.concatenar_trayectos("Ejemplo", "Ayuda", "Concatenado")

    def test_concatenar_trayectos_NoExisteCaminoError(self):
        self.motor.crear_trayecto("Ejemplo", "San Juan, San Juan, Argentina", "Chubut")
        self.motor.crear_trayecto("Ejemplo1", "Roma", "Paris")
        with self.assertRaises(NoExisteCaminoError):
            self.motor.concatenar_trayectos("Ejemplo", "Ejemplo1", "Concatenado")

    def test_comparar_trayectos_exitosamente_por_tiempo(self):
        self.motor.crear_trayecto("BA - La Plata", "Buenos Aires", "La Plata")
        self.motor.crear_trayecto("Tandil - Neuquen", "Tandil", "Neuquen")
        comparacion = self.motor.comparar("BA - La Plata", "Tandil - Neuquen", "t")
        esperado = "Tandil - Neuquen tiene mayor duracion que BA - La Plata\n" \
                   "Tiempo BA - La Plata:  0 dias,  0 horas, 56 min\n" \
                   "Tiempo Tandil - Neuquen:  0 dias, 10 horas, 14 min"
        self.assertEqual(esperado, comparacion)

    def test_comparar_trayectos_exitosamente_por_distancia(self):
        self.motor.crear_trayecto("BA - La Plata", "Buenos Aires", "La Plata")
        self.motor.crear_trayecto("Tandil - Neuquen", "Tandil", "Neuquen")
        comparacion = self.motor.comparar("BA - La Plata", "Tandil - Neuquen", "d")
        esperado = "Tandil - Neuquen es mayor que BA - La Plata\n" \
                   "Distancia BA - La Plata:    58.16 km\n" \
                   "Distancia Tandil - Neuquen:   902.80 km"
        self.assertEqual(esperado, comparacion)

    def test_comparar_trayectos_NoExisteTrayectoError(self):
        with self.assertRaises(NoExisteTrayectoError):
            self.motor.comparar("A", "B", "t")

    def test_comparar_trayectos_ParametroInvalidoError(self):
        self.motor.crear_trayecto("BA - La Plata", "Buenos Aires", "La Plata")
        self.motor.crear_trayecto("Tandil - Neuquen", "Tandil", "Neuquen")
        with self.assertRaises(ParametroInvalidoError):
            self.motor.comparar("BA - La Plata", "Tandil - Neuquen", "X")

    def test_abrir_y_guardar_exitosamente(self):
        self.motor.crear_trayecto("BALP", "Buenos Aires", "La Plata")
        motor2 = MotorDeTrayectos()
        self.motor.guardar()
        motor2.abrir()
        self.assertDictEqual(self.motor.diccionario_de_trayectos, motor2.diccionario_de_trayectos)

    def test_listar_exitosamente(self):
        trayecto1 = self.motor.crear_trayecto("BA - La Plata", "Buenos Aires", "La Plata")
        sleep(1)
        trayecto2 = self.motor.crear_trayecto("Tandil - Neuquen", "Tandil", "Neuquen")
        string_esperado ="'BA - La Plata', 'Tandil - Neuquen'"
        self.assertEqual(string_esperado, self.motor.listar())

    def test_listar_no_hay_trayectos_disponibles(self):
        self.assertEqual("No hay trayectos disponibles", self.motor.listar())


if __name__ == '__main__':
    unittest.main()
