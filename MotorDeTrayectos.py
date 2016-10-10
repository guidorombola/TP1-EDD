import pickle

import googlemaps

from Excepciones import NombreVacioError, NoExisteTrayectoError, NoExisteCaminoError, ParametroInvalidoError
from Formateador import Formateador
from Trayecto import Trayecto
from config import *


class MotorDeTrayectos:
    gmaps = googlemaps.Client(key=KEY)

    def __init__(self):
        self.diccionario_de_trayectos = {}

    def crear_trayecto(self, nombre, ciudad1, ciudad2):
        if nombre.strip() == "":
            raise NombreVacioError("No se ha ingresado un nombre")
        trayecto = Trayecto(nombre, ciudad1, ciudad2)
        self.diccionario_de_trayectos[nombre] = trayecto
        return trayecto

    def agregar_ciudad_al_final(self, nombre_trayecto, ciudad):
        if nombre_trayecto not in self.diccionario_de_trayectos:
            raise NoExisteTrayectoError("El trayecto indicado no se encuentra en la base de datos")
        self.diccionario_de_trayectos[nombre_trayecto].agregar_ciudad_al_final(ciudad)

    def agregar_ciudad(self, nombre_trayecto, ciudad_referencia, ciudad):
        if nombre_trayecto not in self.diccionario_de_trayectos:
            raise NoExisteTrayectoError("El trayecto indicado no se encuentra en la base de datos")
        self.diccionario_de_trayectos[nombre_trayecto].agregar_ciudad(ciudad_referencia, ciudad)

    def concatenar_trayectos(self, trayecto1, trayecto2, nuevo_nombre):
        if trayecto1 not in self.diccionario_de_trayectos or trayecto2 not in self.diccionario_de_trayectos:
            raise NoExisteTrayectoError("Al menos uno de los trayectos no se encuentra en la base de datos")
        destino_trayecto1 = self.diccionario_de_trayectos[trayecto1].lista_de_rutas[-1].destino
        origen_trayecto2 = self.diccionario_de_trayectos[trayecto2].lista_de_rutas[0].origen
        if not Trayecto.existe_camino(self, destino_trayecto1, origen_trayecto2):
            raise NoExisteCaminoError("No existe camino entre el destino del primer trayecto y el origen del segundo")
        if destino_trayecto1 != origen_trayecto2:
            nueva_ruta = Trayecto.crear_ruta(self, destino_trayecto1, origen_trayecto2)
            self.diccionario_de_trayectos[trayecto1].lista_de_rutas.append(nueva_ruta)
        for ruta in self.diccionario_de_trayectos[trayecto2].lista_de_rutas:
            self.diccionario_de_trayectos[trayecto1].lista_de_rutas.append(ruta)
        self.diccionario_de_trayectos.pop(trayecto2)
        self.diccionario_de_trayectos[trayecto1].nombre = nuevo_nombre
        self.diccionario_de_trayectos[nuevo_nombre] = self.diccionario_de_trayectos.pop(trayecto1)

    def comparar(self, trayecto1, trayecto2, parametro):
        if trayecto1 not in self.diccionario_de_trayectos or trayecto2 not in self.diccionario_de_trayectos:
            raise NoExisteTrayectoError("Al menos uno de los trayectos no se encuentra en la base de datos")

        distancia1 = self.diccionario_de_trayectos[trayecto1].distancia_total()
        distancia2 = self.diccionario_de_trayectos[trayecto2].distancia_total()
        tiempo1 = self.diccionario_de_trayectos[trayecto1].tiempo_total()
        tiempo2 = self.diccionario_de_trayectos[trayecto2].tiempo_total()
        distancia1_formateada = Formateador.formateo_distancia(self, distancia1)
        distancia2_formateada = Formateador.formateo_distancia(self, distancia2)
        tiempo1_formateado = Formateador.formateo_tiempo(self, tiempo1)
        tiempo2_formateado = Formateador.formateo_tiempo(self, tiempo2)

        if parametro == "d":
            if distancia1 > distancia2:
                salida = trayecto1 + " es mayor que " + trayecto2
            elif distancia1 < distancia2:
                salida = trayecto2 + " es mayor que " + trayecto1
            else:
                salida = trayecto1 + " y " + trayecto2 + " tienen igual distancia"
            return salida + "\n" + "Distancia {0}: {1:8.2f} km".format(trayecto1, distancia1_formateada) + "\n" + \
                   "Distancia {0}: {1:8.2f} km".format(trayecto2, distancia2_formateada)
        elif parametro == "t":
            if tiempo1 > tiempo2:
                salida = trayecto1 + " tiene mayor duracion que " + trayecto2
            elif tiempo1 < tiempo2:
                salida = trayecto2 + " tiene mayor duracion que " + trayecto1
            else:
                salida = trayecto1 + " Y " + trayecto2 + " tienen igual duracion"
        else:
            raise ParametroInvalidoError("Por favor ingrese un parametro valido")
        return salida + "\n" + "Tiempo {0}: {1:2d} dias, {2:2d} horas, {3:2d} min" \
            .format(trayecto1, tiempo1_formateado[0], tiempo1_formateado[1], tiempo1_formateado[2]) + "\n" + \
               "Tiempo {0}: {1:2d} dias, {2:2d} horas, {3:2d} min". \
                   format(trayecto2, tiempo2_formateado[0], tiempo2_formateado[1], tiempo2_formateado[2])

    def guardar(self):
        with open('persistencia.p', 'wb') as handle:
            pickle.dump(self.diccionario_de_trayectos, handle)

    def abrir(self):
        with open('persistencia.p', 'rb') as handle:
            self.diccionario_de_trayectos = pickle.load(handle)

    def listar(self):
        lista_nombres = []
        for trayecto in self.diccionario_de_trayectos:
            lista_nombres.append(trayecto)
        if len(lista_nombres) == 0:
            return "No hay trayectos disponibles"
        else:
            lista_nombres.sort()
            salida = str(lista_nombres)
            return salida[1:-1]

    def mostrar_trayecto(self, nombre_trayecto):
        if nombre_trayecto not in self.diccionario_de_trayectos:
            raise NoExisteTrayectoError("El trayecto indicado no se encuentra en la base de datos")
        trayecto = self.diccionario_de_trayectos[nombre_trayecto]
        return trayecto.mostrar()

    def mostrar_rutas(self, nombre_trayecto):
        if nombre_trayecto not in self.diccionario_de_trayectos:
            raise NoExisteTrayectoError("El trayecto indicado no se encuentra en la base de datos")
        trayecto = self.diccionario_de_trayectos[nombre_trayecto]
        return trayecto.mostrar_rutas()
