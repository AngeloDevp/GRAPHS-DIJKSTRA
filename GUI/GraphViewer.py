import matplotlib.pyplot as plt
import networkx as nx
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from GUI.PanZoomController import PanZoomController

class GraphViewer:
    def __init__(self):
        # Diccionario maestro de coordenadas (Longitud, Latitud) 
        # basado en las ciudades de tu archivo XML
        self.city_coords = {
            'CCS': (-66.99, 10.60),   # Caracas
            'AUA': (-70.01, 12.50),   # Aruba
            'CUR': (-68.96, 12.19),   # Curazao
            'BON': (-68.28, 12.13),   # Bonaire
            'SXM': (-63.11, 18.04),   # San Martín
            'PAP': (-72.29, 18.58),   # Puerto Príncipe
            'SDQ': (-69.67, 18.43),   # Santo Domingo
            'SBH': (-62.83, 17.90),   # San Bartolomé
            'POS': (-61.34, 10.60),   # Puerto España (Trinidad)
            'BGI': (-59.49, 13.08),   # Barbados
            'PTP': (-61.53, 16.26),   # Guadalupe
            'FDF': (-60.99, 14.59),   # Martinica
        }

    def CreateGraph(self, graphObj, optimalRoute=None):
        fig = plt.Figure(figsize=(12, 6), dpi=100)
        fig.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.02)
        
        # 1. MAGIA DE CARTOPY: Convertimos el gráfico en un mapa geográfico real
        ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
        ax.set_title("Red de Vuelos - Metro Travel", fontweight='bold', pad=15)

        self.interactor = PanZoomController(fig, ax)

        if not graphObj.adjacency:
            # Usamos transform=ax.transAxes para centrar el texto en coordenadas relativas de la ventana
            ax.text(0.5, 0.5, "Cargue los archivos para visualizar el grafo", 
                    ha='center', va='center', transform=ax.transAxes)
            return fig

        # 2. COLOREAR EL MAPA
        # Agregamos océano, tierra, costas y fronteras con colores minimalistas
        ax.add_feature(cfeature.OCEAN, facecolor='#E0F7FA') # Azul muy claro
        ax.add_feature(cfeature.LAND, facecolor='#F5F5F5')  # Gris muy claro
        ax.add_feature(cfeature.COASTLINE, edgecolor='#9E9E9E', linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, edgecolor='#BDBDBD', linestyle=':', linewidth=0.5)

        # 3. ENFOCAR LA CÁMARA EN EL CARIBE
        # Límites geográficos: [Longitud Min, Longitud Max, Latitud Min, Latitud Max]
        ax.set_extent([-75, -55, 9, 20], crs=ccrs.PlateCarree())

        # 4. CONSTRUIR EL GRAFO (No dirigido para no duplicar costos)
        G = nx.Graph()
        for origin, destinations in graphObj.adjacency.items():
            for destination, cost in destinations.items():
                G.add_edge(origin, destination, weight=cost)

        # 5. ASIGNAR COORDENADAS GPS EN LUGAR DE "SPRING_LAYOUT"
        # Mapeamos los nodos del grafo con nuestro diccionario. 
        # Si por error hay una ciudad sin coordenadas, la pone en (0,0) para que no crashee.
        pos = {node: self.city_coords.get(node, (0, 0)) for node in G.nodes()}

        # 6. DIBUJAR LA RED BASE
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', alpha=0.5)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightgray', node_size=400, edgecolors='gray')
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=7, font_weight='bold')

        # 7. DIBUJAR LOS COSTOS (Con caja blanca de fondo)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(
            G, pos, 
            edge_labels=labels, 
            font_size=7, 
            ax=ax,
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1)
        )

        # 8. RESALTAR LA RUTA ÓPTIMA (Si existe)
        if optimalRoute:
            routeEdges = [(optimalRoute[i], optimalRoute[i+1]) for i in range(len(optimalRoute)-1)]
            
            # Línea de ruta (Azul y más gruesa)
            nx.draw_networkx_edges(G, pos, edgelist=routeEdges, edge_color='#1976D2', width=2.5, ax=ax)
            
            # Nodos de escalas (Azules)
            nx.draw_networkx_nodes(G, pos, nodelist=optimalRoute, node_color='#64B5F6', node_size=500, ax=ax)
            
            # Origen (Verde) y Destino (Rojo)
            nx.draw_networkx_nodes(G, pos, nodelist=[optimalRoute[0]], node_color='#81C784', node_size=600, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=[optimalRoute[-1]], node_color='#E57373', node_size=600, ax=ax)

        return fig