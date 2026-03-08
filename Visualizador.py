class Visualizador:
    # Ahora es un método de instancia normal, por eso lleva "self"
    def dibujar_grafo(self, grafo_obj, ruta_optima=None):
        try:
            import networkx as nx
            import matplotlib.pyplot as plt

            G = nx.Graph()
            for origen, destinos in grafo_obj.adyacencia.items():
                for destino, costo in destinos.items():
                    G.add_edge(origen, destino, weight=costo)

            pos = nx.spring_layout(G, seed=42)
            plt.figure(figsize=(10, 6))

            nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=1500, font_weight='bold', font_size=9)
            
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

            if ruta_optima:
                aristas_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
                nx.draw_networkx_nodes(G, pos, nodelist=ruta_optima, node_color='lightblue', node_size=1500)
                nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta, edge_color='blue', width=3.0)

            plt.title("Red de Vuelos Metro Travel - Ruta Óptima")
            plt.axis('off')
            plt.show()
        except ImportError:
            print("\n[INFO] Las librerías 'networkx' y/o 'matplotlib' no están instaladas.")
            print("El cálculo es correcto, pero no se mostrará la interfaz gráfica.")