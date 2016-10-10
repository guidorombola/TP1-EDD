from Formateador import Formateador


class Ruta:
    def __init__(self, origen, destino, distancia, tiempo_de_viaje):
        self.origen = origen
        self.destino = destino
        self.distancia = distancia
        self.tiempo_de_viaje = tiempo_de_viaje

    def __str__(self):
        origen_y_destino = "Origen: " + str(self.origen) + " | Destino: " + str(self.destino)
        distancia_en_km = Formateador.formateo_distancia(self, self.distancia)
        tiempo_formateado = Formateador.formateo_tiempo(self, self.tiempo_de_viaje)
        distancia = "Distancia: " + str(distancia_en_km) + " km"
        tiempo_de_viaje = "Tiempo de viaje: " + "{0} dias, {1} horas, {2} minutos". \
            format(tiempo_formateado[0], tiempo_formateado[1], tiempo_formateado[2])
        return origen_y_destino + "\n" + distancia + "\n" + tiempo_de_viaje + "\n"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
