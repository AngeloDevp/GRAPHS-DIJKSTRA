import tkinter as tk
from GUI.StyleConfig import StyleConfig
from GUI.MapViewer import MapViewer
from GUI.SearchPanel import SearchPanel

class MetroTravelGUI:
    def __init__(self, root, app):
        """
        Orquestador principal de la Interfaz Gráfica.
        :param root: La ventana principal de Tkinter (tk.Tk()).
        :param app: El controlador de la aplicación con la lógica de negocio.
        """
        self.root = root
        self.app = app
        
        # 1. Aplicar configuraciones globales desde StyleConfig
        self.root.title(StyleConfig.WINDOW_TITLE)
        self.root.geometry(StyleConfig.WINDOW_SIZE)
        
        # (Opcional) Configurar un color de fondo base
        self.root.configure(bg=StyleConfig.BG_PANEL_LEFT)
        
        # 2. Instanciar los Componentes Visuales
        # Primero creamos el visor del mapa (Panel Derecho)
        self.map_viewer = MapViewer(self.root, self.app)
        
        # Luego creamos el panel de controles (Panel Izquierdo)
        # Le inyectamos la referencia del 'map_viewer' para que puedan comunicarse
        self.search_panel = SearchPanel(self.root, self.app, self.map_viewer)