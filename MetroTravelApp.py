from Grafo import *
from OptimizadorRutas import *
from LectorDatos import *
from Visualizador import *

class MetroTravelApp:
    def __init__(self):
        # Instanciamos TODAS las clases que necesitamos usar
        self.grafo = Grafo()
        self.optimizador = OptimizadorRutas(self.grafo)
        self.lector = LectorDatos()        # Creamos el objeto lector
        self.visualizador = Visualizador() # Creamos el objeto visualizador

    def inicializar_datos(self, arch_ciudades, arch_vuelos):
        # Usamos el objeto lector instanciado
        dict_ciudades = self.lector.cargar_ciudades(arch_ciudades)
        lista_vuelos = self.lector.cargar_vuelos(arch_vuelos)

        if not dict_ciudades or not lista_vuelos:
            print("[!] Sistema iniciado sin datos. Revise los archivos CSV.")
            return

        for ciudad in dict_ciudades.values():
            self.grafo.agregar_ciudad(ciudad)

        for origen, destino, precio in lista_vuelos:
            self.grafo.agregar_vuelo(origen, destino, precio)

    def ejecutar(self):
        print("="*40)
        print("  SISTEMA DE RUTAS - METRO TRAVEL")
        print("="*40)
        
        while True:
            print("\n--- NUEVA CONSULTA ---")
            origen = input("Ingrese código de ciudad de ORIGEN (ej. CCS) o 'SALIR': ").strip().upper()
            if origen == 'SALIR':
                print("¡Gracias por usar Metro Travel!")
                break
                
            destino = input("Ingrese código de ciudad de DESTINO (ej. SXM): ").strip().upper()
            
            visa_input = input("¿El pasajero posee VISA vigente? (S/N): ").strip().upper()
            tiene_visa = True if visa_input == 'S' else False

            print("\nCriterio de optimización:")
            print("1. Minimizar COSTO del viaje ($)")
            print("2. Minimizar número de ESCALAS")
            opcion = input("Seleccione (1 o 2): ").strip()
            modo = "costo" if opcion == "1" else "escalas"

            ruta, resultado = self.optimizador.calcular_ruta_optima(origen, destino, tiene_visa, modo)

            print("\n" + "="*40)
            print("RESULTADO DE LA BÚSQUEDA:")
            print("="*40)
            
            if ruta is None:
                print(f"[!] {resultado}")
            else:
                str_ruta = " -> ".join(ruta)
                print(f"Ruta a seguir: {str_ruta}")
                
                if modo == "costo":
                    print(f"Costo Total: $ {resultado:.2f}")
                else:
                    print(f"Número de vuelos: {resultado} (Escalas: {resultado - 1})")
                
                # Usamos el objeto visualizador instanciado
                print("\nGenerando mapa visual...")
                self.visualizador.dibujar_grafo(self.grafo, ruta)