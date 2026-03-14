import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from GUI.CRUDForms import CRUDForms
from GUI.StyleConfig import StyleConfig

class SearchPanel:
    def __init__(self, parent, app, mapViewer):
        self.app = app
        self.mapViewer = mapViewer  # referencia al mapa
        self.parent = parent # padre para de las ventanas emergentes
        
        self.origin = tk.StringVar()
        self.destination = tk.StringVar()
        self.requiresVisa = tk.BooleanVar(value=True)
        self.criteria = tk.StringVar(value="cost") # valor predeterminado
        
        # Panel Izquierdo
        self.panel = tk.Frame(parent, width=320, padx=20, pady=20)
        self.panel.pack_propagate(False)
        self.panel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.CreateWidgets()

    def CreateWidgets(self):

        tk.Label(self.panel, text="1. Cargar Datos", font=StyleConfig.FONT_TITLE, fg=StyleConfig.COLOR_PRIMARY).pack(anchor=tk.W, pady=(0, 5))
        
        self.citiesBtn = tk.Button(self.panel, text="📁 Cargar Ciudades", command=self.LoadCities)
        self.citiesBtn.pack(fill=tk.X, pady=5)
        self.citiesLabel = tk.Label(self.panel, text="[Pendiente]", fg="gray", font=StyleConfig.FONT_SMALL)
        self.citiesLabel.pack(anchor=tk.W)

        self.flightsBtn = tk.Button(self.panel, text="📁 Cargar Vuelos", command=self.LoadFlights, state=tk.DISABLED)
        self.flightsBtn.pack(fill=tk.X, pady=5)
        self.flightsLabel = tk.Label(self.panel, text="[Pendiente]", fg="gray", font=StyleConfig.FONT_SMALL)
        self.flightsLabel.pack(anchor=tk.W, pady=(0, 20))

        tk.Frame(self.panel, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # --- SECCIÓN 2: BÚSQUEDA ---
        tk.Label(self.panel, text="2. Buscar Ruta Óptima", font=StyleConfig.FONT_TITLE, fg=StyleConfig.COLOR_PRIMARY).pack(anchor=tk.W, pady=(0, 5))

        tk.Label(self.panel, text="Origen:", font=StyleConfig.FONT_SUBTITLE).pack(anchor=tk.W)
        self.originComboBox = ttk.Combobox(self.panel, textvariable=self.origin, state="disabled")
        self.originComboBox.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.panel, text="Destino:", font=StyleConfig.FONT_SUBTITLE).pack(anchor=tk.W)
        self.destinationComboBox = ttk.Combobox(self.panel, textvariable=self.destination, state="disabled")
        self.destinationComboBox.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.panel, text="¿Tiene Visa?", font=StyleConfig.FONT_SUBTITLE).pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="Sí", variable=self.requiresVisa, value=True).pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="No", variable=self.requiresVisa, value=False).pack(anchor=tk.W, pady=(0, 10))

        # --- SECCIÓN 3: ESTRATEGIA ---
        tk.Label(self.panel, text="Estrategia (Minimizar):", font=StyleConfig.FONT_SUBTITLE).pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="Costo ($)", variable=self.criteria, value="cost").pack(anchor=tk.W)
        tk.Radiobutton(self.panel, text="Escalas", variable=self.criteria, value="scale").pack(anchor=tk.W, pady=(0, 15))

        self.runBtn = tk.Button(self.panel, text="▶ Calcular Ruta", command=self.ExecuteSearch, bg=StyleConfig.COLOR_BUTTON, fg=StyleConfig.COLOR_TEXT_LIGHT, font=StyleConfig.FONT_BUTTON, state=tk.DISABLED)
        self.runBtn.pack(fill=tk.X)

        self.resultFrame = tk.Frame(self.panel)
        self.resultFrame.pack(fill=tk.X, pady=10)

        self.scrollbar = tk.Scrollbar(self.resultFrame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.textResult = tk.Text(self.resultFrame, height=4, width=30, font=StyleConfig.FONT_TEXT,
                                  yscrollcommand=self.scrollbar.set, bg=self.panel.cget("bg"), relief=tk.FLAT)
        self.textResult.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.scrollbar.config(command=self.textResult.yview)

        self.textResult.tag_config("error", foreground="red")
        self.textResult.tag_config("success", foreground="#008000")
        
        self.textResult.config(state=tk.DISABLED)

        tk.Frame(self.panel, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # --- SECCIÓN 4: GESTIÓN DE RED (CRUD) ---
        tk.Label(self.panel, text="4. Gestionar Red", font=StyleConfig.FONT_TITLE, fg=StyleConfig.COLOR_PRIMARY).pack(anchor=tk.W, pady=(0, 5))

        btn_add_city = tk.Button(self.panel, text="➕ Añadir Ciudad")
        btn_del_city = tk.Button(self.panel, text="🗑️ Eliminar Ciudad")
        btn_add_flight = tk.Button(self.panel, text="✈️ Añadir Vuelo")
        btn_mod_flight = tk.Button(self.panel, text="✏️ Modificar Costo")
        btn_del_flight = tk.Button(self.panel, text="❌ Eliminar Vuelo")

        btn_add_city.pack(fill=tk.X, pady=2)
        btn_del_city.pack(fill=tk.X, pady=2)
        btn_add_flight.pack(fill=tk.X, pady=2)
        btn_mod_flight.pack(fill=tk.X, pady=2)
        btn_del_flight.pack(fill=tk.X, pady=2)

        self.crudForms = CRUDForms(self.parent, self.app, self.OnGraphUpdated)
        
        btn_add_city.config(command=self.crudForms.OpenAddCity)
        btn_del_city.config(command=self.crudForms.OpenDeleteCity)
        btn_add_flight.config(command=self.crudForms.OpenAddFlight)
        btn_mod_flight.config(command=self.crudForms.OpenModifyFlight)
        btn_del_flight.config(command=self.crudForms.OpenDeleteFlight)

    def OnGraphUpdated(self):
        options = self.app.GetCitiesList()

        if hasattr(self, 'originComboBox'):
            # Actualiza las ciudades si se agrega una nueva o se elimina alguna existente
            self.originComboBox.config(values=options)
            self.destinationComboBox.config(values=options)
            
            if self.origin.get() and self.origin.get().split(" - ")[0] not in self.app.graph.cities:
                self.originComboBox.set("")

            if self.destination.get() and self.destination.get().split(" - ")[0] not in self.app.graph.cities:
                self.destinationComboBox.set("")

        self.mapViewer.UpdateGraph(None)

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
                options = self.app.GetCitiesList()
                self.originComboBox.config(values=options, state="readonly")
                self.destinationComboBox.config(values=options, state="readonly")
                self.runBtn.config(state=tk.NORMAL)
                
                self.mapViewer.UpdateGraph(None) 
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

        self.textResult.config(state=tk.NORMAL) # Habilitar para escribir
        self.textResult.delete("1.0", tk.END)   # Limpiar búsqueda anterior

        if path is None:
            self.textResult.insert(tk.END, f"Error:\n{result}", "error")
            self.mapViewer.UpdateGraph(None) # Limpiamos el mapa
        else:
            text = f"¡Ruta encontrada!\n\n{' ➔ '.join(path)}\n\n"
            if self.criteria.get() == "cost":
                text += f"Costo Total: $ {result:.2f}"
            else:
                text += f"Número de Vuelos: {result}\n(Escalas: {result - 1})"
            
            self.textResult.insert(tk.END, text, "success")
            self.mapViewer.UpdateGraph(path) # Trazamos la ruta

        self.textResult.config(state=tk.DISABLED) # Volver a bloquear para lectura