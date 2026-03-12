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

    def RemoveCity(self, city_code):
        city_code = city_code.upper()
        
        if city_code in self.cities:
            del self.cities[city_code]
            
        if city_code in self.adjacency:
            del self.adjacency[city_code]
            
        for origin in list(self.adjacency.keys()):
            if city_code in self.adjacency[origin]:
                del self.adjacency[origin][city_code]
                
    def RemoveFlight(self, origin, destination):
        origin = origin.upper()
        destination = destination.upper()
        
        if origin in self.adjacency and destination in self.adjacency[origin]:
            del self.adjacency[origin][destination]

    def UpdateFlightCost(self, origin, destination, new_price):
        origin = origin.upper()
        destination = destination.upper()
        
        if origin in self.adjacency and destination in self.adjacency[origin]:
            self.adjacency[origin][destination] = float(new_price)
            return True
        return False