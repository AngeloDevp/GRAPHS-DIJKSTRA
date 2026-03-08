from LectorDatos import *

class LectorCSV(LectorDatos):
    def cargar_ciudades(self, ruta_archivo):
        print(f"FLAG 3: Cargando ciudades desde {ruta_archivo}")
        ciudades = {}
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                req_visa = True if fila['requiere_visa'].strip().lower() == 'si' else False
                ciudades[fila['codigo']] = Ciudad(fila['codigo'], fila['nombre'], req_visa)
        return ciudades

    def cargar_vuelos(self, ruta_archivo):
        vuelos = []
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                vuelos.append((fila['origen'].strip().upper(), fila['destino'].strip().upper(), float(fila['precio'])))
        
        print(f"FLAG 4: Vuelos cargados desde LECTORCSV {vuelos}")
        return vuelos