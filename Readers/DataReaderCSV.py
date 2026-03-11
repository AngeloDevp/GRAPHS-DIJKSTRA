from Readers.DataReader import *

class DataReaderCSV(DataReader):
    def LoadCities(self, pathFile):
        cities = {}
        with open(pathFile, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for fila in reader:
                requiresVisa = True if fila['requiresVisa'].strip().lower() == 'si' else False
                if fila['code'] not in cities:
                    cities[fila['code']] = City(fila['code'], fila['name'], requiresVisa)
        return cities

    def LoadFlights(self, pathFile):
        flights = []
        with open(pathFile, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for fila in reader:
                origin = fila['origin'].strip().upper()
                destination = fila['destination'].strip().upper()
                price = float(fila['price'])
                if (origin, destination, price) not in flights:  
                    flights.append((origin, destination, price))
                
        return flights