from LectorDatos import *
import json

class LectorJSON(LectorDatos):
    def cargar_ciudades(self, ruta_archivo):
            ciudades = {}
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
                for item in datos:
                    req_visa = True if item['requiere_visa'].strip().lower() == 'si' else False
                    ciudades[item['codigo']] = Ciudad(item['codigo'], item['nombre'], req_visa)
            return ciudades

    def cargar_vuelos(self, ruta_archivo):
        vuelos = []
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            for item in datos:
                vuelos.append((item['origen'].strip().upper(), item['destino'].strip().upper(), float(item['precio'])))
        return vuelos