from FileManager import *
from Graph import *
from Strategies.RouteStrategy import *
from Strategies.RouteStrategyLCS import *
from Strategies.RouteStrategyLSS import *
from GUI.GraphViewer import *
from Strategies.RouteOptimizer import *

class MetroTravelApp:
    def __init__(self):
        self.graph = Graph()
        self.fileManager = FileManager()
        self.routeOptimizer = RouteOptimizer()
        self.graphViewer = GraphViewer()
        self.loadedCities = False
        self.loadedFlights = False

    def ProcessCities(self, pathFile):
        try:
            reader = self.fileManager.GetReader(pathFile)
            dictCities = reader.LoadCities(pathFile)
            self.graph.cities.clear()
            self.graph.adjacency.clear()
            for city in dictCities.values():
                self.graph.AddCity(city)
            self.loadedCities = True

            self.loadedFlights = False # Si recarga cities, debe recargar vuelos
            return True, f"{len(dictCities)} Ciudades cargadas."
        except Exception as e:
            return False, str(e)

    def ProcessFlights(self, pathFile):
        try:
            reader = self.fileManager.GetReader(pathFile)
            flightsList = reader.LoadFlights(pathFile)
            for origin, destination, price in flightsList:
                self.graph.AddFlight(origin, destination, price)
            self.loadedFlights = True

            return True, f"{len(flightsList)} vuelos cargados."
        except Exception as e:
            return False, str(e)

    def GetCitiesList(self):
        options = [f"{c.code} - {c.name}" for c in self.graph.cities.values()]
        options.sort()
        return options

    def ProcessSearch(self, origin, destination, requiresVisa, criteria):
        if criteria == "cost":
            self.routeOptimizer.SetStrategy(RouteStrategyLCS())
        elif criteria == "scale":
            self.routeOptimizer.SetStrategy(RouteStrategyLSS())
            
        return self.routeOptimizer.ExecuteOptimization(self.graph, origin, destination, requiresVisa)

    def GetGraphMap(self, path=None):
        return self.graphViewer.CreateGraph(self.graph, self.graph.cities, path)