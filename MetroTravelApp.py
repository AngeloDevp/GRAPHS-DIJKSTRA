from GestorArchivos import *
from Grafo import *
from EstrategiaRuta import *
from EstrategiaMenorCosto import *
from EstrategiaMenorEscalas import *
from Visualizador import *
from OptimizadorRutas import *

class MetroTravelApp:
    """Controlador Principal de la Aplicación"""
    def __init__(self):
        self.grafo = Grafo()
        self.gestor_archivos = GestorArchivos()
        self.optimizador = OptimizadorRutas()
        self.visualizador = Visualizador()
        self.ciudades_cargadas = False
        self.vuelos_cargados = False

    def procesar_archivo_ciudades(self, ruta_archivo):
        try:
            lector = self.gestor_archivos.obtener_lector(ruta_archivo)
            print(f"FLAG 2: Lector obtenido: {type(lector).__name__}")
            dict_ciudades = lector.cargar_ciudades(ruta_archivo)
            self.grafo.ciudades.clear()
            self.grafo.adyacencia.clear()
            for ciudad in dict_ciudades.values():
                self.grafo.agregar_ciudad(ciudad)
            self.ciudades_cargadas = True
            print(f"FLAG 3: Ciudades cargadas: {list(self.grafo.ciudades.keys())}")

            self.vuelos_cargados = False # Si recarga ciudades, debe recargar vuelos
            return True, f"{len(dict_ciudades)} ciudades cargadas."
        except Exception as e:
            return False, str(e)

    def procesar_archivo_vuelos(self, ruta_archivo):
        try:
            lector = self.gestor_archivos.obtener_lector(ruta_archivo)
            lista_vuelos = lector.cargar_vuelos(ruta_archivo)
            for origen, destino, precio in lista_vuelos:
                self.grafo.agregar_vuelo(origen, destino, precio)
            self.vuelos_cargados = True
            print(f"FLAG 4: Vuelos cargados: {lista_vuelos}, RUTA: {ruta_archivo}")

            return True, f"{len(lista_vuelos)} vuelos cargados."
        except Exception as e:
            return False, str(e)

    def obtener_lista_ciudades(self):
        opciones = [f"{c.codigo} - {c.nombre}" for c in self.grafo.ciudades.values()]
        opciones.sort()
        return opciones

    def procesar_busqueda(self, origen, destino, tiene_visa, criterio):
        # Asignar la Estrategia dinámicamente según el criterio del usuario
        if criterio == "costo":
            self.optimizador.set_estrategia(EstrategiaMenorCosto())
        elif criterio == "escalas":
            self.optimizador.set_estrategia(EstrategiaMenorEscalas())
            
        return self.optimizador.ejecutar_optimizacion(self.grafo, origen, destino, tiene_visa)

    def obtener_figura_mapa(self, ruta=None):
        return self.visualizador.generar_figura(self.grafo, ruta)