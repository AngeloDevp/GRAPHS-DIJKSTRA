from EstrategiaRuta import *

class EstrategiaMenorCosto(EstrategiaRuta):
    """Estrategia que usa Dijkstra minimizando el precio en dólares"""
    def calcular_ruta(self, grafo_obj, origen, destino, tiene_visa):
        return self._ejecutar_dijkstra(grafo_obj, origen, destino, tiene_visa, usar_escalas=False)
        
    def _ejecutar_dijkstra(self, grafo_obj, origen, destino, tiene_visa, usar_escalas):
        distancias = {nodo: float('inf') for nodo in grafo_obj.adyacencia}
        distancias[origen] = 0
        padres = {nodo: None for nodo in grafo_obj.adyacencia}
        nodos_no_visitados = list(grafo_obj.adyacencia.keys())

        while nodos_no_visitados:
            nodo_actual = min(nodos_no_visitados, key=lambda nodo: distancias[nodo])

            if distancias[nodo_actual] == float('inf') or nodo_actual == destino:
                break

            nodos_no_visitados.remove(nodo_actual)

            for vecino, costo_vuelo in grafo_obj.adyacencia[nodo_actual].items():
                if grafo_obj.ciudades[vecino].requiere_visa and not tiene_visa:
                    continue

                # La magia de la estrategia ocurre aquí: Costo real vs Valor 1
                peso = 1 if usar_escalas else costo_vuelo
                nueva_distancia = distancias[nodo_actual] + peso

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = nodo_actual

        if distancias[destino] == float('inf'):
            return None, "No existe ruta dadas las restricciones de visa."

        camino = []
        actual = destino
        while actual is not None:
            camino.insert(0, actual)
            actual = padres[actual]

        return camino, distancias[destino]