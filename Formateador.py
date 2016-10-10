import unicodedata


class Formateador:
    def formateo_tiempo(self, tiempo):
        dias = int(tiempo / 24 / 60 / 60)
        tiempo = tiempo - dias * 24 * 60 * 60
        horas = int(tiempo / 60 / 60)
        tiempo = tiempo - horas * 60 * 60
        min = int(tiempo / 60)
        return dias, horas, min

    def formateo_distancia(self, distancia):
        return distancia / 1000

    def estandarizar_texto(self, texto):
        texto_salida = ''.join(c for c in unicodedata.normalize('NFD', texto)
                               if unicodedata.category(c) != 'Mn')
        return texto_salida
