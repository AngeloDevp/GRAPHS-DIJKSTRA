from Strategies.RouteStrategyLCS import *

class RouteStrategyLSS(RouteStrategyLCS):
    def RouteCalculator(self, graphObj, origin, destination, requiresVisa):
        return self.RunDijkstra(graphObj, origin, destination, requiresVisa, useScales=True)