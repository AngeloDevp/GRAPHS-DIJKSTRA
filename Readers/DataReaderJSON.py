from DataReader import *
import json

class DataReaderJSON(DataReader):
    def LoadCities(self, pathFile):
            cities = {}
            with open(pathFile, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    requiresVisa = True if item['requiresVisa'].strip().lower() == 'si' else False
                    cities[item['code']] = City(item['code'], item['name'], requiresVisa)
            return cities

    def LoadFlights(self, pathFile):
        flights = []
        with open(pathFile, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                flights.append((item['origin'].strip().upper(), item['destination'].strip().upper(), float(item['price'])))
        return flights