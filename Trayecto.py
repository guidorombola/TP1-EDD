import googlemaps

from Excepciones import NoExisteCaminoError, CiudadInexistenteError
from Formateador import Formateador
from Ruta import Ruta
from config import *


class Trayecto:
    gmaps = googlemaps.Client(key=KEY)

    def __init__(self, nombre, ciudad1, ciudad2):
        self.lista_de_rutas = []
        if not self.existe_camino(ciudad1, ciudad2):
            raise NoExisteCaminoError('No existe ruta entre estas ciudades')
        self.lista_de_rutas.append(self.crear_ruta(ciudad1, ciudad2))
        self.nombre = nombre

    def crear_ruta(self, ciudad1, ciudad2):
        matriz_ruta = self.gmaps.distance_matrix(ciudad1, ciudad2, language="es")
        origen = matriz_ruta["origin_addresses"][0]
        destino = matriz_ruta["destination_addresses"][0]
        duracion = matriz_ruta["rows"][0]["elements"][0]["duration"]["value"]
        distancia = matriz_ruta["rows"][0]["elements"][0]["distance"]["value"]
        ruta = Ruta(origen, destino, distancia, duracion)
        return ruta

    def existe_camino(self, ciudad1, ciudad2):
        ruta = self.gmaps.distance_matrix(ciudad1, ciudad2, language="es")
        return ruta["rows"][0]["elements"][0]["status"] == "OK"

    def agregar_ciudad_al_final(self, ciudad):
        ultima_ciudad = self.lista_de_rutas[-1].destino
        if not self.existe_camino(ultima_ciudad, ciudad):
            raise NoExisteCaminoError('No existe ruta entre estas ciudades')
        ruta_a_agregar = self.crear_ruta(ultima_ciudad, ciudad)
        self.lista_de_rutas.append(ruta_a_agregar)

    def agregar_ciudad(self, ciudad_referencia, ciudad_a_agregar):
        encontro = False
        for i, ruta in enumerate(self.lista_de_rutas):
            ruta_estandarizada = Formateador.estandarizar_texto(self, ruta.destino)
            ruta_formateada = ruta_estandarizada.lower().split(", ")
            input_formateado = Formateador.estandarizar_texto(self, ciudad_referencia)
            if ruta_formateada[0] == input_formateado.lower().split(", ")[0]:
                if not self.existe_camino(ruta.origen, ciudad_a_agregar) or not self.existe_camino(ciudad_a_agregar,
                                                                                                   ciudad_referencia):
                    raise NoExisteCaminoError('No existe ruta entre estas ciudades')
                ruta1 = self.crear_ruta(ruta.origen, ciudad_a_agregar)
                ruta2 = self.crear_ruta(ciudad_a_agregar, ciudad_referencia)
                self.lista_de_rutas[i] = ruta1
                self.lista_de_rutas.insert(i + 1, ruta2)
                encontro = True
                break
        if not encontro:
            raise CiudadInexistenteError("No existe la ciudad")

    def tiempo_total(self):
        suma = 0
        for x in self.lista_de_rutas:
            suma += x.tiempo_de_viaje
        return suma

    def distancia_total(self):
        suma = 0
        for x in self.lista_de_rutas:
            suma += x.distancia
        return suma

    def mostrar(self):
        ciudades = []
        ciudades.append(self.lista_de_rutas[0].origen)
        ciudades.append(self.lista_de_rutas[0].destino)
        for i in range(1, len(self.lista_de_rutas), 1):
            ciudades.append(self.lista_de_rutas[i].destino)
        salida1 = "Ciudades: " + str(ciudades)[1:-1]
        salida2 = "Distancia total: " + str(Formateador.formateo_distancia(self, self.distancia_total())) + " km"
        tiempo = Formateador.formateo_tiempo(self, self.tiempo_total())
        salida3 = "Tiempo estimado: {0} dias {1} horas {2} minutos".format(tiempo[0], tiempo[1], tiempo[2])
        return self.nombre + "\n" + salida1 + "\n" + salida2 + "\n" + salida3 + "\n"

    def mostrar_rutas(self):
        salida = ""
        for ruta in self.lista_de_rutas:
            salida += ruta.__str__() + "\n"
        return salida

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
