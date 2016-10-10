import unittest

import googlemaps

from Excepciones import *
from Trayecto import Trayecto
from config import *
from time import sleep


class TrayectoTest(unittest.TestCase):

    def setUp(self):
        sleep(1)
        self.trayecto = Trayecto("BALP", "Buenos Aires", "La Plata")

    def tearDown(self):
        self.trayecto = None

    def test_crear_trayecto_exitosamente(self):
        lista = []
        lista.append(Trayecto.crear_ruta(self.trayecto, "Buenos Aires", "La Plata"))
        self.assertListEqual(lista, self.trayecto.lista_de_rutas)

    def test_NoExisteCaminoError(self):
        with self.assertRaises(NoExisteCaminoError):
            baires_madrid = Trayecto("Baires-Madrid", "Buenos Aires", "Madrid")

    def test_existe_camino(self):
        self.assertTrue(Trayecto.existe_camino(self.trayecto, "Buenos Aires", "Tandil"))

    def test_no_existe_camino(self):
        self.assertFalse(Trayecto.existe_camino(self.trayecto, "Cordoba", "Moscu"))

    def test_agregar_ciudad_al_final_exitosamente(self):
        trayectoLocal = Trayecto("BALP", "Buenos Aires", "La Plata")
        trayectoLocal.agregar_ciudad_al_final("Tandil")
        lista = []
        lista.append(Trayecto.crear_ruta(trayectoLocal, "Buenos Aires", "La Plata"))
        lista.append(Trayecto.crear_ruta(trayectoLocal, "La Plata", "Tandil"))
        self.assertListEqual(lista, trayectoLocal.lista_de_rutas)

    def test_agregar_ciudad_al_final_NoExisteCaminoError(self):
        with self.assertRaises(NoExisteCaminoError):
            trayectoLocal = Trayecto("BALP", "Buenos Aires", "La Plata")
            trayectoLocal.agregar_ciudad_al_final("Berlin")

    def test_agregar_ciudad_exitosamente(self):
        trayectoLocal = Trayecto("BALP", "Buenos Aires", "La Plata")
        trayectoLocal.agregar_ciudad("La Plata", "Tandil")
        lista = []
        lista.append(Trayecto.crear_ruta(trayectoLocal, "Buenos Aires", "Tandil"))
        lista.append(Trayecto.crear_ruta(trayectoLocal, "Tandil", "La Plata"))
        self.assertListEqual(lista, trayectoLocal.lista_de_rutas)

    def test_agregar_ciudad_CiudadInexistenteError(self):
        trayectoLocal = Trayecto("BALP", "Buenos Aires", "La Plata")
        with self.assertRaises(CiudadInexistenteError):
            trayectoLocal.agregar_ciudad("Tokio", "Tandil")

    def test_agregar_ciudad_NoExisteCaminoError(self):
        trayectoLocal = Trayecto("BALP", "Buenos Aires", "La Plata")
        with self.assertRaises(NoExisteCaminoError):
            trayectoLocal.agregar_ciudad("La Plata", "Manila")


if __name__ == "__main__":
    unittest.main()
