import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SearchPanel:
    def __init__(self, parent, app, map_viewer):
        """
        :param parent: La ventana o frame padre donde se alojará este panel.
        :param app: El controlador principal (lógica de negocio).
        :param map_viewer: Referencia al visor del mapa para ordenarle actualizarse.
        """
        self.app = app
        self.map_viewer = map_viewer  # Guardamos la referencia al mapa
        
        # Variables de estado de la UI
        self.origin = tk.StringVar()
        self.destination = tk.StringVar()
        self.requiresVisa = tk.BooleanVar(value=True)
        self.criteria = tk.StringVar(value="cost")
        
        # Crear el contenedor visual (Panel Izquierdo)
        self.panel = tk.Frame(parent, width=320, padx=20, pady=20)
        self.panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Construir los botones y formularios
        self.CreateWidgets()

    def CreateWidgets(self):
        # --- SECCIÓN 1: CARGA DE ARCHIVOS ---
        tk.Label(self.panel, text="1. Cargar Datos", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 10))
        
        self.citiesBtn = tk.Button(self.panel, text="📁 Cargar Ciudades", command=self.LoadCities)
        self.citiesBtn.pack(fill=tk.X, pady=5)
        self.citiesLabel = tk.Label(self.panel, text="[Pendiente]", fg="gray", font=("Arial", 8))
        self.citiesLabel.pack(anchor=tk.W)

        self.flightsBtn = tk.Button(self.panel, text="📁 Cargar Vuelos", command=self.LoadFlights, state=tk.DISABLED)
        self.flightsBtn.pack(fill=tk.X, pady=5)
        self.flightsLabel = tk.Label(self.panel, text="[Pendiente]", fg="gray", font=("Arial", 8))
        self.flightsLabel.pack(anchor=tk.W, pady=(0, 20))

        tk.Frame(self.panel, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # --- SECCIÓN 2: BÚSQUEDA ---
        tk.Label(self.panel, text="2. Buscar Ruta Óptima", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 10))

        tk.Label(self.panel, text="Origen:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.originComboBox = ttk.Combobox(self.panel, textvariable=self.origin, state="disabled")
        self.originComboBox.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.panel, text="Destino:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.destinationComboBox = ttk.Combobox(self.panel, textvariable=self.destination, state="disabled")
        self.destinationComboBox.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.panel, text="¿Tiene Visa?", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="Sí", variable=self.requiresVisa, value=True).pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="No", variable=self.requiresVisa, value=False).pack(anchor=tk.W, pady=(0, 10))

        # --- SELECCIÓN DE ESTRATEGIA ---
        tk.Label(self.panel, text="Estrategia (Minimizar):", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="Costo ($)", variable=self.criteria, value="cost").pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="Escalas", variable=self.criteria, value="scale").pack(anchor=tk.W, pady=(0, 15))

        self.runBtn = tk.Button(self.panel, text="▶ Calcular Ruta", command=self.ExecuteSearch, bg="#0052cc", fg="white", font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.runBtn.pack(fill=tk.X)

        self.labelResult = tk.Label(self.panel, text="", font=("Arial", 10), justify=tk.LEFT, wraplength=260)
        self.labelResult.pack(anchor=tk.W, pady=15)

    def LoadCities(self):
        path = filedialog.askopenfilename(title="Seleccionar Archivo de Ciudades", filetypes=[("Archivos Soportados", "*.csv;*.json;*.xml")])
        if path:
            success, msj = self.app.ProcessCities(path)
            if success:
                self.citiesLabel.config(text=f"✅ {msj}", fg="green")
                self.flightsBtn.config(state=tk.NORMAL)
                # Reseteamos la búsqueda
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
                options = self.app.GetCitiesList()
                self.originComboBox.config(values=options, state="readonly")
                self.destinationComboBox.config(values=options, state="readonly")
                self.runBtn.config(state=tk.NORMAL)
                
                # ¡AQUÍ ESTÁ LA MAGIA! Le decimos al visor que se actualice.
                self.map_viewer.UpdateGraph(None) 
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
            origin=originCode, destination=destinationCode,
            requiresVisa=self.requiresVisa.get(), criteria=self.criteria.get()
        )

        if path is None:
            self.labelResult.config(text=f"❌ Error:\n{result}", fg="red")
            self.map_viewer.UpdateGraph(None) # Limpiamos el mapa en caso de error
        else:
            text = f"✅ ¡Ruta encontrada!\n\n{' ➔ '.join(path)}\n\n"
            if self.criteria.get() == "cost":
                text += f"Costo Total: $ {result:.2f}"
            else:
                text += f"Número de Vuelos: {result}\n(Escalas: {result - 1})"
            
            self.labelResult.config(text=text, fg="green")
            self.map_viewer.UpdateGraph(path) # Trazamos la ruta ganadora