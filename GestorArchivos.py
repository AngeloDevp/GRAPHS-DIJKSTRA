from LectorCSV import *
from LectorJSON import *   
from LectorXML import *

class GestorArchivos:
    def obtener_lector(self, ruta_archivo):
            if ruta_archivo.endswith('.csv'): return LectorCSV()
            elif ruta_archivo.endswith('.json'): return LectorJSON()
            elif ruta_archivo.endswith('.xml'): return LectorXML()
            else: raise ValueError("Formato de archivo no soportado.")