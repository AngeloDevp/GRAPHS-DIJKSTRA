from MetroTravelApp import *

class Main:
    # Ahora es un método normal
    def run(self):
        app = MetroTravelApp()
        app.inicializar_datos("ciudades.csv", "vuelos.csv")
        app.ejecutar()

# ==========================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================
if __name__ == "__main__":
    # Como la clase Main ya no tiene métodos estáticos, 
    # estamos obligados a instanciarla (crear el objeto "programa")
    programa = Main()
    programa.run()