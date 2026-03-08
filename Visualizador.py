import networkx as nx
import matplotlib.pyplot as plt

class Visualizador:
    def generar_figura(self, grafo_obj, ruta_optima=None):
        """Crea y devuelve un objeto Figure de Matplotlib sin abrir ventanas nuevas"""
        fig = plt.Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title("Red de Vuelos - Metro Travel")

        G = nx.Graph()
        for origen, destinos in grafo_obj.adyacencia.items():
            for destino, costo in destinos.items():
                G.add_edge(origen, destino, weight=costo)

        pos = nx.spring_layout(G, seed=42)
        
        # Dibujar grafo base
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightgray', node_size=800, font_size=8, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7, ax=ax)

        # Resaltar la ruta si existe
        if ruta_optima:
            aristas_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
            nx.draw_networkx_nodes(G, pos, nodelist=ruta_optima, node_color='lightblue', node_size=800, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta, edge_color='blue', width=2.5, ax=ax)

        return fig