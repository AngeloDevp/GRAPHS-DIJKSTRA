class OptimizadorRutas:

    def __init__(self, grafo):
            self.grafo = grafo

    def calcular_ruta_optima(self, origen, destino, tiene_visa, modo="costo"):
        """
        Implementación del Algoritmo de Dijkstra desde cero.
        """
        # Validaciones iniciales
        if origen not in self.grafo.adyacencia or destino not in self.grafo.adyacencia:
            return None, "Origen o destino inválidos o no existen en la red."
        
        # Validar regla del enunciado: no puede empezar en destino con visa si no la tiene
        if self.grafo.ciudades[origen].requiere_visa and not tiene_visa:
            return None, "No puede iniciar el viaje: no tiene visa para la ciudad de origen."

        distancias = {nodo: float('inf') for nodo in self.grafo.adyacencia}
        distancias[origen] = 0
        padres = {nodo: None for nodo in self.grafo.adyacencia}
        nodos_no_visitados = list(self.grafo.adyacencia.keys())

        while nodos_no_visitados:
            nodo_actual = min(nodos_no_visitados, key=lambda nodo: distancias[nodo])

            if distancias[nodo_actual] == float('inf'):
                break
            
            if nodo_actual == destino:
                break

            nodos_no_visitados.remove(nodo_actual)

            for vecino, costo in self.grafo.adyacencia[nodo_actual].items():
                ciudad_vecina = self.grafo.ciudades[vecino]
                
                # Regla de negocio: Si el destino requiere visa y no la tiene, ignoramos la ruta
                if ciudad_vecina.requiere_visa and not tiene_visa:
                    continue

                # Determinar si minimizamos costo ($) o escalas (saltos de valor 1)
                peso = costo if modo == "costo" else 1
                nueva_distancia = distancias[nodo_actual] + peso

                # Relajación de la arista
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    padres[vecino] = nodo_actual

        # Reconstrucción del camino óptimo
        if distancias[destino] == float('inf'):
            return None, "No existe una ruta posible hacia el destino con las condiciones actuales."

        camino = []
        actual = destino
        while actual is not None:
            camino.insert(0, actual)
            actual = padres[actual]

        return camino, distancias[destino]