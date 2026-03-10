from DataReader import *

class DataReaderCSV(DataReader):
    def LoadCities(self, pathFile):
        cities = {}
        with open(pathFile, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for fila in reader:
                requiresVisa = True if fila['requiresVisa'].strip().lower() == 'si' else False
                cities[fila['code']] = City(fila['code'], fila['name'], requiresVisa)
        return cities

    def LoadFlights(self, pathFile):
        flights = []
        with open(pathFile, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for fila in reader:
                flights.append((fila['origin'].strip().upper(), fila['destination'].strip().upper(), float(fila['price'])))
    
        return flights