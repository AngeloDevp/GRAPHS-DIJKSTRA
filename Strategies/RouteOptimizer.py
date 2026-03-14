class RouteOptimizer:
    def __init__(self):
        self.currentStrategy = None

    def SetStrategy(self, strategy):
        self.currentStrategy = strategy

    def ExecuteOptimization(self, graphObj, origin, destination, requiresVisa):
        if not self.currentStrategy:
            return None, "Error: No se ha definido una estrategia de optimización."
        
        if origin not in graphObj.adjacency or destination not in graphObj.adjacency:
            return None, "Origen o destino inválidos."
        if graphObj.cities[origin].requiresVisa and not requiresVisa:
            return None, "No puede iniciar el viaje: no tiene visa para el origen."
            
        return self.currentStrategy.RouteCalculator(graphObj, origin, destination, requiresVisa)