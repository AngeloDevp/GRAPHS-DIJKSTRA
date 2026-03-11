from Readers.DataReader import *

class DataReaderJSON(DataReader):
    def LoadCities(self, pathFile):
            cities = {}
            with open(pathFile, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    requiresVisa = True if item['requiresVisa'].strip().lower() == 'si' else False
                    if item['code'] not in cities:
                        cities[item['code']] = City(item['code'], item['name'], requiresVisa)
            return cities

    def LoadFlights(self, pathFile):
        flights = []
        with open(pathFile, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                origin = item['origin'].strip().upper()
                destination = item['destination'].strip().upper()
                price = float(item['price'])
                if (origin, destination, price) not in flights:
                    flights.append((origin, destination, price))
        return flights