import tkinter as tk
from tkinter import messagebox, ttk

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False

class MetroTravelGUI:
    """
    Esta clase SOLO maneja botones, ventanas y clicks. 
    Delega todo el trabajo pesado a la clase 'app'.
    """
    def __init__(self, root, app):
        self.root = root
        self.app = app # Recibimos la instancia de MetroTravelApp
        
        self.root.title("Metro Travel - Optimización de Rutas")
        self.root.geometry("900x600")
        
        # Variables de Tkinter
        self.var_origen = tk.StringVar()
        self.var_destino = tk.StringVar()
        self.var_visa = tk.BooleanVar(value=True)
        self.var_criterio = tk.StringVar(value="costo")
        
        # Construir Interfaz
        self.crear_widgets()

    def crear_widgets(self):
        # Panel Izquierdo (Controles)
        panel_controles = tk.Frame(self.root, width=300, padx=20, pady=20)
        panel_controles.pack(side=tk.LEFT, fill=tk.Y)
        
        # Le pedimos la lista de ciudades a la App
        opciones_ciudades = self.app.obtener_lista_ciudades()

        tk.Label(panel_controles, text="Ciudad de Origen:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        cb_origen = ttk.Combobox(panel_controles, textvariable=self.var_origen, values=opciones_ciudades, state="readonly", width=30)
        cb_origen.pack(anchor=tk.W, pady=(0, 15))

        tk.Label(panel_controles, text="Ciudad de Destino:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        cb_destino = ttk.Combobox(panel_controles, textvariable=self.var_destino, values=opciones_ciudades, state="readonly", width=30)
        cb_destino.pack(anchor=tk.W, pady=(0, 15))

        tk.Label(panel_controles, text="¿El pasajero posee Visa?", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        tk.Radiobutton(panel_controles, text="Sí posee", variable=self.var_visa, value=True).pack(anchor=tk.W)
        tk.Radiobutton(panel_controles, text="No posee", variable=self.var_visa, value=False).pack(anchor=tk.W, pady=(0, 15))

        tk.Label(panel_controles, text="Criterio de Búsqueda:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        tk.Radiobutton(panel_controles, text="Minimizar Costo ($)", variable=self.var_criterio, value="costo").pack(anchor=tk.W)
        tk.Radiobutton(panel_controles, text="Minimizar Escalas", variable=self.var_criterio, value="escalas").pack(anchor=tk.W, pady=(0, 20))

        btn_ejecutar = tk.Button(panel_controles, text="Buscar Ruta Óptima", command=self.ejecutar_busqueda, bg="#0052cc", fg="white", font=("Arial", 12, "bold"))
        btn_ejecutar.pack(fill=tk.X, pady=10)

        self.lbl_resultado = tk.Label(panel_controles, text="", font=("Arial", 10), justify=tk.LEFT, wraplength=260)
        self.lbl_resultado.pack(anchor=tk.W, pady=20)

        # Panel Derecho (Gráfico)
        self.panel_grafico = tk.Frame(self.root, bg="white")
        self.panel_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Dibujar gráfico inicial vacío (le pedimos la figura a la App)
        self.actualizar_grafico(None)

    def ejecutar_busqueda(self):
        origen_seleccionado = self.var_origen.get()
        destino_seleccionado = self.var_destino.get()

        if not origen_seleccionado or not destino_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un origen y un destino.")
            return

        origen_codigo = origen_seleccionado.split(" - ")[0]
        destino_codigo = destino_seleccionado.split(" - ")[0]

        # ¡AQUÍ ESTÁ LA MAGIA DEL DESACOPLAMIENTO!
        # La GUI no sabe cómo funciona Dijkstra, solo le hace la pregunta a la App:
        ruta, resultado = self.app.procesar_busqueda(
            origen=origen_codigo,
            destino=destino_codigo,
            tiene_visa=self.var_visa.get(),
            modo=self.var_criterio.get()
        )

        # Mostrar resultados en texto
        if ruta is None:
            self.lbl_resultado.config(text=f"❌ Error:\n{resultado}", fg="red")
            self.actualizar_grafico(None)
        else:
            texto = f"✅ ¡Ruta encontrada!\n\nCamino:\n{' ➔ '.join(ruta)}\n\n"
            if self.var_criterio.get() == "costo":
                texto += f"Costo Total: $ {resultado:.2f}"
            else:
                texto += f"Número de Vuelos: {resultado}\n(Escalas: {resultado - 1})"
            
            self.lbl_resultado.config(text=texto, fg="green")
            self.actualizar_grafico(ruta)

    def actualizar_grafico(self, ruta_optima):
        if not GRAFICOS_DISPONIBLES:
            tk.Label(self.panel_grafico, text="Librerías gráficas no instaladas.\nNo se puede mostrar el mapa.").pack()
            return

        for widget in self.panel_grafico.winfo_children():
            widget.destroy()

        # Le pedimos a la App que nos dé la imagen (figura) del mapa
        fig = self.app.obtener_figura_mapa(ruta_optima)

        canvas = FigureCanvasTkAgg(fig, master=self.panel_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)