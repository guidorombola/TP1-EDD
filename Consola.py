import pickle
import sys

import googlemaps.exceptions

from Excepciones import *
from MotorDeTrayectos import MotorDeTrayectos


class Consola:
    def __init__(self):
        self.motor = MotorDeTrayectos()

    def principal(self):
        while True:
            print("MENU PRINCIPAL\n")
            print("1- Crear trayecto")
            print("2- Agregar una ciudad al final de un trayecto")
            print("3- Agregar una ciudad intermedia a un trayecto")
            print("4- Concatenar dos trayectos")
            print("5- Comparar dos trayectos")
            print("6- Mostrar un trayecto")
            print("7- Mostrar rutas que componen un trayecto")
            print("8- Listar los trayectos calculados")
            print("9- Guardar trayectos calculados")
            print("10- Recuperar del disco trayectos almacenados")
            print("11- Salir y guardar")
            try:
                opcionMenu = input("Ingrese la opción que desea\n")
                if opcionMenu == "1":
                    self.crear_trayecto()
                elif opcionMenu == "2":
                    self.agregar_ciudad_al_final()
                elif opcionMenu == "3":
                    self.agregar_ciudad_intermedia()
                elif opcionMenu == "4":
                    self.concatenar_trayectos()
                elif opcionMenu == "5":
                    self.comparar_dos_trayectos()
                elif opcionMenu == "6":
                    self.mostrar_un_trayecto()
                elif opcionMenu == "7":
                    self.mostrar_rutas()
                elif opcionMenu == "8":
                    self.listar_trayectos()
                elif opcionMenu == "9":
                    self.guardar_trayectos()
                elif opcionMenu == "10":
                    self.recuperar_trayectos()
                elif opcionMenu == "11":
                    self.salir_y_guardar()
                else:
                    print("La opcion ingresada no es valida\n\n")
            except (googlemaps.exceptions.TransportError, googlemaps.exceptions.ApiError,
                    googlemaps.exceptions.HTTPError, googlemaps.exceptions._RetriableRequest,
                    googlemaps.exceptions.Timeout):
                print("Error de Google Maps. Intente mas tarde.")

    def crear_trayecto(self):
        nombre = input("\nIngrese nombre trayecto\n")
        ciudad1 = input("Ingrese ciudad origen\n")
        ciudad2 = input("Ingrese ciudad destino\n")
        try:
            self.motor.crear_trayecto(nombre, ciudad1, ciudad2)
        except NoExisteCaminoError:
            print(sys.exc_info()[1])
            self.crear_trayecto()
        except NombreVacioError:
            print(sys.exc_info()[1])
            self.crear_trayecto()
        else:
            print("El trayecto se ha agregado exitosamente\n")
            self.principal()

    def agregar_ciudad_al_final(self):
        self.listar_trayectos()
        nombre = input("\nIngrese nombre de trayecto\n")
        ciudad = input("Ingrese ciudad a agregar\n")
        try:
            self.motor.agregar_ciudad_al_final(nombre, ciudad)
        except NoExisteTrayectoError:
            print(sys.exc_info()[1])
            self.agregar_ciudad_al_final()
        else:
            print("Ciudad agregada exitosamente\n")
            self.principal()

    def agregar_ciudad_intermedia(self):
        self.listar_trayectos()
        nombre = input("\nIngrese nombre de trayecto\n")
        ciudad_ref = input("Ingrese ciudad posterior a la que desea agregar\n")
        ciudad_a_agregar = input("Ingrese ciudad a agregar")
        try:
            self.motor.agregar_ciudad(nombre, ciudad_ref, ciudad_a_agregar)
        except NoExisteTrayectoError:
            print(sys.exc_info()[1])
            self.agregar_ciudad_intermedia()
        else:
            print("Ciudad agregada exitosamente\n")
            self.principal()

    def concatenar_trayectos(self):
        self.listar_trayectos()
        trayecto1 = input("\nIngrese el nombre del primer trayecto a concatenar\n")
        trayecto2 = input("Ingrese el nombre del segundo trayecto a concatenar\n")
        nuevo_nombre = input("Ingrese el nuevo nombre que recibirá el trayecto concatenado\n")
        try:
            self.motor.concatenar_trayectos(trayecto1, trayecto2, nuevo_nombre)
        except NoExisteTrayectoError:
            print(sys.exc_info()[1])
            self.concatenar_trayectos()
        except NoExisteCaminoError:
            print(sys.exc_info()[1])
            self.concatenar_trayectos()
        else:
            print("Los trayectos se concatenaron exitosamente\n")
            self.principal()

    def comparar_dos_trayectos(self):
        self.listar_trayectos()
        trayecto1 = input("\nIngrese el nombre del primer trayecto a comparar\n")
        trayecto2 = input("Ingrese el nombre del segundo trayecto a comparar\n")
        parametro = input("Desea comparar por: \n (d) Distancia \n (t) Tiempo \n")
        try:
            print(self.motor.comparar(trayecto1, trayecto2, parametro))
        except NoExisteTrayectoError:
            print(sys.exc_info()[1])
            self.comparar_dos_trayectos()
        except ParametroInvalidoError:
            print(sys.exc_info()[1])
            self.comparar_dos_trayectos()
        else:
            self.principal()

    def mostrar_un_trayecto(self):
        self.listar_trayectos()
        trayecto = input("\nIngrese el nombre del trayecto a mostrar\n")
        try:
            print(self.motor.mostrar_trayecto(trayecto))
        except NoExisteTrayectoError:
            print(sys.exc_info()[1])
            self.mostrar_un_trayecto()
        else:
            self.principal()

    def mostrar_rutas(self):
        self.listar_trayectos()
        trayecto = input("\nIngrese el nombre del trayecto a mostrar\n")
        try:
            print(self.motor.mostrar_rutas(trayecto))
        except NoExisteTrayectoError:
            print(sys.exc_info()[1])
            self.mostrar_rutas()
        else:
            self.principal()

    def listar_trayectos(self):
        print("\nLos trayectos almacenados son: ")
        print(self.motor.listar())

    def guardar_trayectos(self):
        self.motor.guardar()
        print("\nLos trayectos se han guardado exitosamente\n")

    def recuperar_trayectos(self):
        try:
            self.motor.abrir()
        except pickle.PickleError:
            print("\nNo se pudo recuperar el archivo correctamente\n")
        else:
            print("\nTrayectos recuperados exitosamente\n")
        finally:
            self.principal()

    def salir_y_guardar(self):
        self.guardar_trayectos()
        print("\n*** PROGRAMA FINALIZADO ***\n")
        exit()


if __name__ == '__main__':
    c = Consola()
    c.principal()
