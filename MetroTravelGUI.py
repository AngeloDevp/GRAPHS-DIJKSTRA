import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


try:
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    GRAFICOS_DISPONIBLES = True
except ImportError:
    GRAFICOS_DISPONIBLES = False


class MetroTravelGUI:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.root.title("Metro Travel - Arquitectura MVC + Patrones")
        self.root.geometry("950x650")
        
        self.origin = tk.StringVar()
        self.destination = tk.StringVar()
        self.requiresVisa = tk.BooleanVar(value=True)
        self.criteria = tk.StringVar(value="cost")
        
        self.CreateWidgets()

    def CreateWidgets(self):
        leftPanel = tk.Frame(self.root, width=320, padx=20, pady=20)
        leftPanel.pack(side=tk.LEFT, fill=tk.Y)
        
        # --- SECCIÓN 1: CARGA DE ARCHIVOS (Patrón Adapter) ---
        tk.Label(leftPanel, text="1. Cargar Datos", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 10))
        
        self.citiesBtn = tk.Button(leftPanel, text="📁 Cargar Ciudades (CSV/JSON/XML)", command=self.LoadCities)
        self.citiesBtn.pack(fill=tk.X, pady=5)
        self.citiesLabel = tk.Label(leftPanel, text="[Pendiente]", fg="gray", font=("Arial", 8))
        self.citiesLabel.pack(anchor=tk.W)

        self.flightsBtn = tk.Button(leftPanel, text="📁 Cargar Vuelos (CSV/JSON/XML)", command=self.LoadFlights, state=tk.DISABLED)
        self.flightsBtn.pack(fill=tk.X, pady=5)
        self.flightsLabel = tk.Label(leftPanel, text="[Pendiente]", fg="gray", font=("Arial", 8))
        self.flightsLabel.pack(anchor=tk.W, pady=(0, 20))

        tk.Frame(leftPanel, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # --- SECCIÓN 2: BÚSQUEDA ---
        tk.Label(leftPanel, text="2. Buscar path Óptima", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 10))

        tk.Label(leftPanel, text="Origen:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.originComboBox = ttk.Combobox(leftPanel, textvariable=self.origin, state="disabled")
        self.originComboBox.pack(fill=tk.X, pady=(0, 10))

        tk.Label(leftPanel, text="Destino:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.destinationComboBox = ttk.Combobox(leftPanel, textvariable=self.destination, state="disabled")
        self.destinationComboBox.pack(fill=tk.X, pady=(0, 10))

        tk.Label(leftPanel, text="¿Tiene Visa?", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        tk.Radiobutton(leftPanel, text="Sí", variable=self.requiresVisa, value=True).pack(anchor=tk.W)
        tk.Radiobutton(leftPanel, text="No", variable=self.requiresVisa, value=False).pack(anchor=tk.W, pady=(0, 10))

        # --- SELECCIÓN DE ESTRATEGIA (Patrón Strategy) ---
        tk.Label(leftPanel, text="Estrategia (Minimizar):", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        tk.Radiobutton(leftPanel, text="Costo ($)", variable=self.criteria, value="cost").pack(anchor=tk.W)
        tk.Radiobutton(leftPanel, text="Escalas", variable=self.criteria, value="scale").pack(anchor=tk.W, pady=(0, 15))

        self.runBtn = tk.Button(leftPanel, text="▶ Calcular path", command=self.ExecuteSearch, bg="#0052cc", fg="white", font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.runBtn.pack(fill=tk.X)

        self.labelResult = tk.Label(leftPanel, text="", font=("Arial", 10), justify=tk.LEFT, wraplength=260)
        self.labelResult.pack(anchor=tk.W, pady=15)

        # --- PANEL DERECHO: GRÁFICO ---
        self.graphicPanel = tk.Frame(self.root, bg="white")
        self.graphicPanel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.UpdateGraph(None)

    def LoadCities(self):
        path = filedialog.askopenfilename(title="Seleccionar Archivo de Ciudades", filetypes=[("Archivos Soportados", "*.csv;*.json;*.xml")])

        if path:
            success, msj = self.app.ProcessCities(path)
            if success:
                self.citiesLabel.config(text=f"✅ {msj}", fg="green")
                self.flightsBtn.config(state=tk.NORMAL)
                self.originComboBox.set("")
                self.destinationComboBox.set("")
                self.originComboBox.config(state=tk.DISABLED)
                self.destinationComboBox.config(state=tk.DISABLED)
                self.runBtn.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", f"No se pudo cargar: {msj}")

    def LoadFlights(self):
        path = filedialog.askopenfilename(title="Seleccionar Archivo de Vuelos", filetypes=[("Archivos Soportados", "*.csv;*.json;*.xml")])
        if path:
            success, msj = self.app.ProcessFlights(path)
            if success:
                self.flightsLabel.config(text=f"✅ {msj}", fg="green")
                # Activar la interfaz de búsqueda
                options = self.app.GetCitiesList()
                self.originComboBox.config(values=options, state="readonly")
                self.destinationComboBox.config(values=options, state="readonly")
                self.runBtn.config(state=tk.NORMAL)
                self.UpdateGraph(None) # Dibujar el grafo base recién cargado
            else:
                messagebox.showerror("Error", f"No se pudo cargar: {msj}")

    def ExecuteSearch(self):
        originSelected = self.origin.get()
        destinationSelected = self.destination.get()

        if not originSelected or not destinationSelected:
            messagebox.showwarning("Aviso", "Seleccione Origen y Destino.")
            return

        originCode = originSelected.split(" - ")[0]
        destinationCode = destinationSelected.split(" - ")[0]

        path, result = self.app.ProcessSearch(
            origin=originCode,
            destination=destinationCode,
            requiresVisa=self.requiresVisa.get(),
            criteria=self.criteria.get()
        )

        if path is None:
            self.labelResult.config(text=f"❌ Error:\n{result}", fg="red")
            self.UpdateGraph(None)
        else:
            text = f"✅ ¡path encontrada!\n\n{' ➔ '.join(path)}\n\n"
            if self.criteria.get() == "cost":
                text += f"Costo Total: $ {result:.2f}"
            else:
                text += f"Número de Vuelos: {result}\n(Escalas: {result - 1})"
            
            self.labelResult.config(text=text, fg="green")
            self.UpdateGraph(path)

    def UpdateGraph(self, path_optima):
        if not GRAFICOS_DISPONIBLES:
            return

        # Limpiar el panel antes de redibujar
        for widget in self.graphicPanel.winfo_children():
            widget.destroy()

        fig = self.app.GetGraphMap(path_optima)
        
        # 1. Crear el canvas
        canvas = FigureCanvasTkAgg(fig, master=self.graphicPanel)
        canvas.draw()
        
        # 2. Crear y empaquetar la barra de herramientas interactiva
        toolbar = NavigationToolbar2Tk(canvas, self.graphicPanel)
        toolbar.update()
        
        # 3. Mostrar el canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)