from Readers.DataReader import *

class DataReaderXML(DataReader):
    def LoadCities(self, pathFile):
        cities = {}
        tree = ET.parse(pathFile)
        root = tree.getroot()

        for item in root.findall('city'):
            code = item.find('code').text
            name = item.find('name').text
            requiresVisa = True if item.find('requiresVisa').text.strip().lower() == 'si' else False
            if code not in cities:
                cities[code] = City(code, name, requiresVisa)
            
        return cities

    def LoadFlights(self, pathFile):
        flights = []
        tree = ET.parse(pathFile)
        root = tree.getroot()
        
        for item in root.findall('flight'):
            origin = item.find('origin').text.strip().upper()
            destination = item.find('destination').text.strip().upper()
            price = float(item.find('price').text)
            if (origin, destination, price) not in flights:
                flights.append((origin, destination, price))
            
        return flights