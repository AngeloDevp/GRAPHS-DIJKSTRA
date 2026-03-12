import matplotlib.pyplot as plt
import networkx as nx
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from GUI.PanZoomController import PanZoomController

class GraphViewer:
    def __init__(self):
        pass

    # 1. Agregamos cities_dict a los parámetros
    def CreateGraph(self, graphObj, cities_dict, optimalRoute=None):
        fig = plt.Figure(figsize=(12, 6), dpi=100)
        fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.02)
        
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        ax.set_title("Red de Vuelos - Metro Travel", fontweight='bold', pad=15)

        self.interactor = PanZoomController(fig, ax)

        if not graphObj.adjacency:
            ax.text(0.5, 0.5, "Cargue los archivos para visualizar el grafo", 
                    ha='center', va='center', transform=ax.transAxes)
            return fig

        # 2. COLOREAR EL MAPA
        ax.add_feature(cfeature.OCEAN, facecolor='#E0F7FA')
        ax.add_feature(cfeature.LAND, facecolor='#F5F5F5')
        ax.add_feature(cfeature.COASTLINE, edgecolor='#9E9E9E', linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, edgecolor='#BDBDBD', linestyle=':', linewidth=0.5)

        # 3. CONSTRUIR EL GRAFO 
        G = nx.Graph()
        for origin, destinations in graphObj.adjacency.items():
            for destination, cost in destinations.items():
                G.add_edge(origin, destination, weight=cost)

        # ==========================================
        # 4. ASIGNAR COORDENADAS DINÁMICAS
        # ==========================================
        pos = {}
        for node in G.nodes():
            if node in cities_dict:
                # Extraemos la tupla de coordenadas de tu objeto City
                pos[node] = cities_dict[node].coordinates
            else:
                pos[node] = (0, 0) # Fallback de seguridad

        # ==========================================
        # 5. CÁMARA DINÁMICA (Auto-Encuadre)
        # ==========================================
        # Extraemos todas las longitudes (X) y latitudes (Y)
        lons = [coords[0] for coords in pos.values() if coords != (0,0)]
        lats = [coords[1] for coords in pos.values() if coords != (0,0)]
        
        if lons and lats:
            padding = 2.0 # Grados de margen para que los nodos no queden pegados al borde
            ax.set_extent([
                min(lons) - padding, max(lons) + padding, 
                min(lats) - padding, max(lats) + padding
            ], crs=ccrs.PlateCarree())

        # 6. DIBUJAR LA RED BASE
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', alpha=0.5)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightgray', node_size=400, edgecolors='gray')
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight='bold')

        # 7. DIBUJAR LOS COSTOS
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=labels, font_size=7, ax=ax,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1)
        )

        # 8. RESALTAR LA RUTA ÓPTIMA
        if optimalRoute:
            routeEdges = [(optimalRoute[i], optimalRoute[i+1]) for i in range(len(optimalRoute)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=routeEdges, edge_color='#1976D2', width=2.5, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=optimalRoute, node_color='#64B5F6', node_size=500, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=[optimalRoute[0]], node_color='#81C784', node_size=600, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=[optimalRoute[-1]], node_color='#E57373', node_size=600, ax=ax)

        return fig