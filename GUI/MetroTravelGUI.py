import tkinter as tk
from GUI.StyleConfig import StyleConfig
from GUI.MapViewer import MapViewer
from GUI.SearchPanel import SearchPanel

class MetroTravelGUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        
        self.root.title(StyleConfig.WINDOW_TITLE)
        self.root.geometry(StyleConfig.WINDOW_SIZE)
        self.root.configure(bg=StyleConfig.BG_PANEL_LEFT)
        
        self.mapViewer = MapViewer(self.root, self.app)        
        self.searchPanel = SearchPanel(self.root, self.app, self.mapViewer)