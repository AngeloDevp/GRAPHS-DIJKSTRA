class Grafo:
    def __init__(self):
        self.ciudades = {}      # { 'CCS': Objeto Ciudad }
        self.adyacencia = {}    # { 'CCS': {'AUA': 40.0, 'CUR': 35.0} }

    def agregar_ciudad(self, ciudad):
        self.ciudades[ciudad.codigo] = ciudad
        if ciudad.codigo not in self.adyacencia:
            self.adyacencia[ciudad.codigo] = {}

    def agregar_vuelo(self, origen, destino, precio):
        # El grafo es no dirigido (el enunciado dice: "el monto en sentido contrario es el mismo")
        if origen in self.adyacencia and destino in self.adyacencia:
            self.adyacencia[origen][destino] = precio
            self.adyacencia[destino][origen] = precio
