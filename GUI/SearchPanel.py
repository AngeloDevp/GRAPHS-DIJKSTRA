import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from GUI.CRUDForms import CRUDForms

class SearchPanel:
    def __init__(self, parent, app, map_viewer):
        """
        :param parent: La ventana o frame padre donde se alojará este panel.
        :param app: El controlador principal (lógica de negocio).
        :param map_viewer: Referencia al visor del mapa para ordenarle actualizarse.
        """
        self.app = app
        self.map_viewer = map_viewer  # Guardamos la referencia al mapa
        self.parent = parent # Guardamos el parent para las ventanas emergentes
        
        # Variables de estado de la UI
        self.origin = tk.StringVar()
        self.destination = tk.StringVar()
        self.requiresVisa = tk.BooleanVar(value=True)
        self.criteria = tk.StringVar(value="cost")
        
        # Crear el contenedor visual (Panel Izquierdo)
        self.panel = tk.Frame(parent, width=320, padx=20, pady=20)
        self.panel.pack_propagate(False)
        self.panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Construir los botones y formularios
        self.CreateWidgets()

    def CreateWidgets(self):
        # --- SECCIÓN 1: CARGA DE ARCHIVOS ---
        tk.Label(self.panel, text="1. Cargar Datos", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 5))
        
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
        tk.Label(self.panel, text="2. Buscar Ruta Óptima", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 5))

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

        self.resultFrame = tk.Frame(self.panel)
        self.resultFrame.pack(fill=tk.X, pady=10)

        self.scrollbar = tk.Scrollbar(self.resultFrame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.textResult = tk.Text(self.resultFrame, height=4, width=30, font=("Arial", 10), 
                                  yscrollcommand=self.scrollbar.set, bg=self.panel.cget("bg"), relief=tk.FLAT)
        self.textResult.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.scrollbar.config(command=self.textResult.yview)

        self.textResult.tag_config("error", foreground="red")
        self.textResult.tag_config("success", foreground="#008000")
        
        self.textResult.config(state=tk.DISABLED)

        tk.Frame(self.panel, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # --- SECCIÓN 3: GESTIÓN DE RED (CRUD) ---
        tk.Label(self.panel, text="3. Gestionar Red", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 5))
        
        # 1. Crear los botones físicos en la interfaz
        btn_add_city = tk.Button(self.panel, text="➕ Añadir Ciudad")
        btn_del_city = tk.Button(self.panel, text="🗑️ Eliminar Ciudad")
        btn_add_flight = tk.Button(self.panel, text="✈️ Añadir Vuelo")
        btn_mod_flight = tk.Button(self.panel, text="✏️ Modificar Costo")
        btn_del_flight = tk.Button(self.panel, text="❌ Eliminar Vuelo")

        # 2. Empaquetarlos
        btn_add_city.pack(fill=tk.X, pady=2)
        btn_del_city.pack(fill=tk.X, pady=2)
        btn_add_flight.pack(fill=tk.X, pady=2)
        btn_mod_flight.pack(fill=tk.X, pady=2)
        btn_del_flight.pack(fill=tk.X, pady=2)

        # 3. Instanciar CRUDForms pasándole nuestra función OnGraphUpdated
        self.crud_forms = CRUDForms(self.parent, self.app, self.OnGraphUpdated)
        
        # 4. Conectar los botones con las funciones de CRUDForms
        btn_add_city.config(command=self.crud_forms.OpenAddCity)
        btn_del_city.config(command=self.crud_forms.OpenDeleteCity)
        btn_add_flight.config(command=self.crud_forms.OpenAddFlight)
        btn_mod_flight.config(command=self.crud_forms.OpenModifyFlight)
        btn_del_flight.config(command=self.crud_forms.OpenDeleteFlight)

    def OnGraphUpdated(self):
        """
        Esta función se ejecuta cada vez que el CRUD modifica el grafo.
        Actualiza las listas desplegables y redibuja el mapa.
        """
        # 1. Actualizar los valores de los Combobox con la nueva lista de ciudades
        options = self.app.GetCitiesList()
        if hasattr(self, 'originComboBox'):
            self.originComboBox.config(values=options)
            self.destinationComboBox.config(values=options)
            
            # Limpiar selección actual si la ciudad fue eliminada
            if self.origin.get() and self.origin.get().split(" - ")[0] not in self.app.graph.cities:
                self.originComboBox.set("")
            if self.destination.get() and self.destination.get().split(" - ")[0] not in self.app.graph.cities:
                self.destinationComboBox.set("")

        # 2. Ordenar al mapa que se redibuje (Pasamos None para limpiar rutas óptimas previas)
        self.map_viewer.UpdateGraph(None)

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

        # --- AQUÍ INYECTAMOS EL RESULTADO EN EL CUADRO DE TEXTO ---
        self.textResult.config(state=tk.NORMAL) # Habilitar para escribir
        self.textResult.delete("1.0", tk.END)   # Limpiar búsqueda anterior

        if path is None:
            self.textResult.insert(tk.END, f"❌ Error:\n{result}", "error")
            self.map_viewer.UpdateGraph(None) # Limpiamos el mapa
        else:
            text = f"✅ ¡Ruta encontrada!\n\n{' ➔ '.join(path)}\n\n"
            if self.criteria.get() == "cost":
                text += f"Costo Total: $ {result:.2f}"
            else:
                text += f"Número de Vuelos: {result}\n(Escalas: {result - 1})"
            
            self.textResult.insert(tk.END, text, "success")
            self.map_viewer.UpdateGraph(path) # Trazamos la ruta

        self.textResult.config(state=tk.DISABLED) # Volver a bloquear para lectura