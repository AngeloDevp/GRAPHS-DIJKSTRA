from DataReader import *
import xml.etree.ElementTree as ET

class DataReaderXML(DataReader):
    def LoadCities(self, pathFile):
        cities = {}
        tree = ET.parse(pathFile)
        root = tree.getroot()
        
        # CAMBIO AQUÍ: Buscamos 'ciudad' en lugar de 'item'
        for item in root.findall('city'):
            code = item.find('code').text
            name = item.find('name').text
            # Manejamos el texto para evitar errores por espacios o mayúsculas
            requiresVisa = True if item.find('requieresVisa').text.strip().lower() == 'si' else False
            cities[code] = City(code, name, requiresVisa)
            
        return cities

    def LoadFlights(self, pathFile):
        flights = []
        tree = ET.parse(pathFile)
        root = tree.getroot()
        
        # CAMBIO AQUÍ: Buscamos 'flight' en lugar de 'item'
        for item in root.findall('flight'):
            origin = item.find('origin').text.strip().upper()
            destination = item.find('destination').text.strip().upper()
            price = float(item.find('price').text)
            flights.append((origin, destination, price))
            
        return flights