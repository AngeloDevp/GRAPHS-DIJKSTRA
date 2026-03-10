class Graph:
    def __init__(self):
        self.cities = {}      # { 'CCS': Objeto city }
        self.adjacency = {}    # { 'CCS': {'AUA': 40.0, 'CUR': 35.0} }

    def AddCity(self, city):
        self.cities[city.code] = city
        if city.code not in self.adjacency:
            self.adjacency[city.code] = {}

    def AddFlight(self, origin, destination, price):
        if origin in self.adjacency and destination in self.adjacency:
            self.adjacency[origin][destination] = price
            self.adjacency[destination][origin] = price
