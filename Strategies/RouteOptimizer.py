class RouteOptimizer:
    """Contexto del Patrón Strategy"""
    def __init__(self):
        self.currentStrategy = None

    def SetStrategy(self, strategy):
        self.currentStrategy = strategy

    def ExecuteOptimization(self, graphObj, origin, destination, requiresVisa):
        if not self.currentStrategy:
            return None, "Error: No se ha definido una strategy de optimización."
        
        # Validación de reglas de negocio globales
        if origin not in graphObj.adjacency or destination not in graphObj.adjacency:
            return None, "Origin o destination inválidos."
        if graphObj.cities[origin].requiresVisa and not requiresVisa:
            return None, "No puede iniciar el viaje: no tiene visa para el origin."
            
        return self.currentStrategy.RouteCalculator(graphObj, origin, destination, requiresVisa)