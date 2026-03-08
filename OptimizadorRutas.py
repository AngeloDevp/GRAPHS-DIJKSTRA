class OptimizadorRutas:
    """Contexto del Patrón Strategy"""
    def __init__(self):
        self.estrategia_actual = None

    def set_estrategia(self, estrategia):
        self.estrategia_actual = estrategia

    def ejecutar_optimizacion(self, grafo_obj, origen, destino, tiene_visa):
        if not self.estrategia_actual:
            return None, "Error: No se ha definido una estrategia de optimización."
        
        # Validación de reglas de negocio globales
        if origen not in grafo_obj.adyacencia or destino not in grafo_obj.adyacencia:
            return None, "Origen o destino inválidos."
        if grafo_obj.ciudades[origen].requiere_visa and not tiene_visa:
            return None, "No puede iniciar el viaje: no tiene visa para el origen."
            
        return self.estrategia_actual.calcular_ruta(grafo_obj, origen, destino, tiene_visa)