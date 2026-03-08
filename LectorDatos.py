import csv
from Ciudad import *   

class LectorDatos:
    def cargar_ciudades(self, ruta_archivo):
        ciudades_leidas = {}
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    codigo = fila['codigo']
                    nombre = fila['nombre']
                    req_visa = True if fila['requiere_visa'].strip().lower() == 'si' else False
                    ciudades_leidas[codigo] = Ciudad(codigo, nombre, req_visa)
            return ciudades_leidas
        except FileNotFoundError:
            return {}

    def cargar_vuelos(self, ruta_archivo):
        vuelos_leidos = []
        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    origen = fila['origen'].strip().upper()
                    destino = fila['destino'].strip().upper()
                    precio = float(fila['precio'])
                    vuelos_leidos.append((origen, destino, precio))
            return vuelos_leidos
        except FileNotFoundError:
            return []