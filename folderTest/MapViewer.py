import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Manejo de la disponibilidad de la librería
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False

class MapViewer:
    def __init__(self, parent_frame, app):
        """
        Inicializa el visor del mapa.
        :param parent_frame: El frame de Tkinter donde se incrustará el mapa.
        :param app: La referencia al controlador principal para obtener los datos.
        """
        self.app = app
        
        # Creamos el contenedor principal para el gráfico
        self.graphicPanel = tk.Frame(parent_frame, bg="white")
        self.graphicPanel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Dibujamos un mapa vacío al inicio
        self.UpdateGraph(None)

    def UpdateGraph(self, path_optima):
        """
        Actualiza el lienzo de Matplotlib con la nueva ruta.
        """
        if not GRAFICOS_DISPONIBLES:
            # Podrías agregar un Label indicando que faltan librerías
            tk.Label(self.graphicPanel, text="Librerías gráficas no disponibles.").pack(expand=True)
            return

        # 1. Limpiar el panel antes de redibujar para no solapar mapas
        for widget in self.graphicPanel.winfo_children():
            widget.destroy()

        # 2. Pedirle la figura generada al Controlador (app)
        fig = self.app.GetGraphMap(path_optima)
        
        # 3. Crear el canvas de Matplotlib y empaquetarlo
        canvas = FigureCanvasTkAgg(fig, master=self.graphicPanel)
        canvas.draw()
        
        # 4. Crear y empaquetar la barra de herramientas interactiva (Zoom, Guardar, etc.)
        toolbar = NavigationToolbar2Tk(canvas, self.graphicPanel)
        toolbar.update()
        
        # 5. Mostrar el canvas en la interfaz
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)