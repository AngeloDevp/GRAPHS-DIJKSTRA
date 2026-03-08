from EstrategiaMenorCosto import *

class EstrategiaMenorEscalas(EstrategiaMenorCosto):
    """Estrategia que usa Dijkstra asumiendo que todos los vuelos valen 1 (Minimiza escalas)"""
    def calcular_ruta(self, grafo_obj, origen, destino, tiene_visa):
        # Reutilizamos el algoritmo base de Dijkstra, pero le indicamos que evalúe escalas
        return self._ejecutar_dijkstra(grafo_obj, origen, destino, tiene_visa, usar_escalas=True)