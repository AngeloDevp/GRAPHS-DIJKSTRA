from Grafo import *
from OptimizadorRutas import *
from LectorDatos import *
from Visualizador import *

class MetroTravelApp:
    """
    Esta clase maneja el estado de la aplicación. 
    No sabe nada de Tkinter ni de interfaces gráficas.
    """
    def __init__(self):
        self.grafo = Grafo()
        self.optimizador = OptimizadorRutas(self.grafo)
        self.lector = LectorDatos()
        self.visualizador = Visualizador()

    def inicializar_datos(self, arch_ciudades, arch_vuelos):
        dict_ciudades = self.lector.cargar_ciudades(arch_ciudades)
        lista_vuelos = self.lector.cargar_vuelos(arch_vuelos)

        if not dict_ciudades or not lista_vuelos:
            return False # Falló la carga

        for ciudad in dict_ciudades.values():
            self.grafo.agregar_ciudad(ciudad)

        for origen, destino, precio in lista_vuelos:
            self.grafo.agregar_vuelo(origen, destino, precio)
            
        return True # Carga exitosa

    def obtener_lista_ciudades(self):
        """Retorna una lista formateada para los menús desplegables de la GUI"""
        opciones = [f"{c.codigo} - {c.nombre}" for c in self.grafo.ciudades.values()]
        opciones.sort()
        return opciones

    def procesar_busqueda(self, origen, destino, tiene_visa, modo):
        """Recibe los datos limpios, llama al algoritmo y retorna el resultado"""
        return self.optimizador.calcular_ruta_optima(origen, destino, tiene_visa, modo)
        
    def obtener_figura_mapa(self, ruta=None):
        """Pide al visualizador que genere el mapa y lo devuelve a la GUI"""
        return self.visualizador.generar_figura(self.grafo, ruta)