import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False

class MapViewer:
    def __init__(self, parent_frame, app):
        self.app = app
        
        self.graphicPanel = tk.Frame(parent_frame, bg="white")
        self.graphicPanel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.UpdateGraph(None)

    def UpdateGraph(self, path_optima):
        if not GRAFICOS_DISPONIBLES:
            tk.Label(self.graphicPanel, text="Librerías gráficas no disponibles.").pack(expand=True)
            return

        for widget in self.graphicPanel.winfo_children():
            widget.destroy()

        fig = self.app.GetGraphMap(path_optima)
        
        canvas = FigureCanvasTkAgg(fig, master=self.graphicPanel)
        canvas.draw()
        
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)