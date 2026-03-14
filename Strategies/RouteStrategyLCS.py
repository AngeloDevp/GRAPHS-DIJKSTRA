from Strategies.RouteStrategy import *

class RouteStrategyLCS(RouteStrategy):

    def RouteCalculator(self, graphObj, origin, destination, requiresVisa):
        return self.RunDijkstra(graphObj, origin, destination, requiresVisa, useScales=False)
        
    def RunDijkstra(self, graphObj, origin, destination, requiresVisa, useScales):
        distances = {}
        parents = {}

        for node in graphObj.adjacency:
            distances[node] = float(99999)
            parents[node] = None
        
        distances[origin] = 0
        unvisitedNodes = list(graphObj.adjacency.keys())

        while unvisitedNodes:
            currentNode = min(unvisitedNodes, key=lambda node: distances[node])

            if distances[currentNode] == float(99999) or currentNode == destination:
                break

            unvisitedNodes.remove(currentNode)

            for neighbor, flightCost in graphObj.adjacency[currentNode].items():
                if graphObj.cities[neighbor].requiresVisa and not requiresVisa: #hasVisa
                    continue

                weight = 1 if useScales else flightCost
                newDistance = distances[currentNode] + weight

                if newDistance < distances[neighbor]:
                    distances[neighbor] = newDistance
                    parents[neighbor] = currentNode

        if distances[destination] == float(99999):
            return None, "No existe ruta dadas las restricciones de visa."

        path = []
        current = destination
        while current is not None:
            path.insert(0, current)
            current = parents[current]

        return path, distances[destination]