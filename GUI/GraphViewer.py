import matplotlib.pyplot as plt
import networkx as nx

class GraphViewer:
    def CreateGraph(self, graphObj, optimalRoute=None):
        fig = plt.Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title("Red de Vuelos - Metro Travel")

        if not graphObj.adjacency:
            ax.text(0.5, 0.5, "Cargue los archivos para visualizar el grafo", ha='center', va='center')
            return fig

        G = nx.Graph()
        for origin, destinations in graphObj.adjacency.items():
            for destination, cost in destinations.items():
                G.add_edge(origin, destination, weight=cost)

        pos = nx.spring_layout(G, seed=42, k=0.85)
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightgray', node_size=600, font_size=8, font_weight='bold')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7, ax=ax)

        if optimalRoute:
            routeEdges = [(optimalRoute[i], optimalRoute[i+1]) for i in range(len(optimalRoute)-1)]
            nx.draw_networkx_nodes(G, pos, nodelist=optimalRoute, node_color='lightblue', node_size=800, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=routeEdges, edge_color='blue', width=2.5, ax=ax)

        return fig