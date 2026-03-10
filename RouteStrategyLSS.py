from RouteStrategyLCS import *

class RouteStrategyLSS(RouteStrategyLCS):
    """Estrategia que usa Dijkstra asumiendo que todos los vuelos valen 1 (Minimiza escalas)"""
    def RouteCalculator(self, graphObj, origin, destination, requiresVisa):
        # Reutilizamos el algoritmo base de Dijkstra, pero le indicamos que evalúe escalas
        return self.RunDijkstra(graphObj, origin, destination, requiresVisa, useScales=True)