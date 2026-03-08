from LectorDatos import *
import xml.etree.ElementTree as ET

class LectorXML(LectorDatos):
    def cargar_ciudades(self, ruta_archivo):
        ciudades = {}
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()
        
        # CAMBIO AQUÍ: Buscamos 'ciudad' en lugar de 'item'
        for item in raiz.findall('ciudad'):
            codigo = item.find('codigo').text
            nombre = item.find('nombre').text
            # Manejamos el texto para evitar errores por espacios o mayúsculas
            req_visa = True if item.find('requiere_visa').text.strip().lower() == 'si' else False
            ciudades[codigo] = Ciudad(codigo, nombre, req_visa)
            
        return ciudades

    def cargar_vuelos(self, ruta_archivo):
        vuelos = []
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()
        
        # CAMBIO AQUÍ: Buscamos 'vuelo' en lugar de 'item'
        for item in raiz.findall('vuelo'):
            origen = item.find('origen').text.strip().upper()
            destino = item.find('destino').text.strip().upper()
            precio = float(item.find('precio').text)
            vuelos.append((origen, destino, precio))
            
        return vuelos