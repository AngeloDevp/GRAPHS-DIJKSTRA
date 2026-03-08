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
        
        self.var_origen = tk.StringVar()
        self.var_destino = tk.StringVar()
        self.var_visa = tk.BooleanVar(value=True)
        self.var_criterio = tk.StringVar(value="costo")
        
        self.crear_widgets()

    def crear_widgets(self):
        panel_izquierdo = tk.Frame(self.root, width=320, padx=20, pady=20)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y)
        
        # --- SECCIÓN 1: CARGA DE ARCHIVOS (Patrón Adapter) ---
        tk.Label(panel_izquierdo, text="1. Cargar Datos", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 10))
        
        self.btn_ciudades = tk.Button(panel_izquierdo, text="📁 Cargar Ciudades (CSV/JSON/XML)", command=self.cargar_ciudades)
        self.btn_ciudades.pack(fill=tk.X, pady=5)
        self.lbl_estado_ciudades = tk.Label(panel_izquierdo, text="[Pendiente]", fg="gray", font=("Arial", 8))
        self.lbl_estado_ciudades.pack(anchor=tk.W)

        self.btn_vuelos = tk.Button(panel_izquierdo, text="📁 Cargar Vuelos (CSV/JSON/XML)", command=self.cargar_vuelos, state=tk.DISABLED)
        self.btn_vuelos.pack(fill=tk.X, pady=5)
        self.lbl_estado_vuelos = tk.Label(panel_izquierdo, text="[Pendiente]", fg="gray", font=("Arial", 8))
        self.lbl_estado_vuelos.pack(anchor=tk.W, pady=(0, 20))

        tk.Frame(panel_izquierdo, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # --- SECCIÓN 2: BÚSQUEDA ---
        tk.Label(panel_izquierdo, text="2. Buscar Ruta Óptima", font=("Arial", 12, "bold"), fg="navy").pack(anchor=tk.W, pady=(0, 10))

        tk.Label(panel_izquierdo, text="Origen:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.cb_origen = ttk.Combobox(panel_izquierdo, textvariable=self.var_origen, state="disabled")
        self.cb_origen.pack(fill=tk.X, pady=(0, 10))

        tk.Label(panel_izquierdo, text="Destino:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.cb_destino = ttk.Combobox(panel_izquierdo, textvariable=self.var_destino, state="disabled")
        self.cb_destino.pack(fill=tk.X, pady=(0, 10))

        tk.Label(panel_izquierdo, text="¿Tiene Visa?", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        tk.Radiobutton(panel_izquierdo, text="Sí", variable=self.var_visa, value=True).pack(anchor=tk.W)
        tk.Radiobutton(panel_izquierdo, text="No", variable=self.var_visa, value=False).pack(anchor=tk.W, pady=(0, 10))

        # --- SELECCIÓN DE ESTRATEGIA (Patrón Strategy) ---
        tk.Label(panel_izquierdo, text="Estrategia (Minimizar):", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        tk.Radiobutton(panel_izquierdo, text="Costo ($)", variable=self.var_criterio, value="costo").pack(anchor=tk.W)
        tk.Radiobutton(panel_izquierdo, text="Escalas", variable=self.var_criterio, value="escalas").pack(anchor=tk.W, pady=(0, 15))

        self.btn_ejecutar = tk.Button(panel_izquierdo, text="▶ Calcular Ruta", command=self.ejecutar_busqueda, bg="#0052cc", fg="white", font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.btn_ejecutar.pack(fill=tk.X)

        self.lbl_resultado = tk.Label(panel_izquierdo, text="", font=("Arial", 10), justify=tk.LEFT, wraplength=260)
        self.lbl_resultado.pack(anchor=tk.W, pady=15)

        # --- PANEL DERECHO: GRÁFICO ---
        self.panel_grafico = tk.Frame(self.root, bg="white")
        self.panel_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.actualizar_grafico(None)

    def cargar_ciudades(self):
        ruta = filedialog.askopenfilename(title="Seleccionar Archivo de Ciudades", filetypes=[("Archivos Soportados", "*.csv;*.json;*.xml")])

        if ruta:
            exito, msj = self.app.procesar_archivo_ciudades(ruta)
            print(f"FLAG 4: RESULTADO DE CARGA: Éxito={exito}, Mensaje='{msj}'")
            if exito:
                self.lbl_estado_ciudades.config(text=f"✅ {msj}", fg="green")
                self.btn_vuelos.config(state=tk.NORMAL)
                self.cb_origen.set("")
                self.cb_destino.set("")
                self.cb_origen.config(state=tk.DISABLED)
                self.cb_destino.config(state=tk.DISABLED)
                self.btn_ejecutar.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", f"No se pudo cargar: {msj}")

    def cargar_vuelos(self):
        ruta = filedialog.askopenfilename(title="Seleccionar Archivo de Vuelos", filetypes=[("Archivos Soportados", "*.csv;*.json;*.xml")])
        if ruta:
            exito, msj = self.app.procesar_archivo_vuelos(ruta)
            if exito:
                self.lbl_estado_vuelos.config(text=f"✅ {msj}", fg="green")
                # Activar la interfaz de búsqueda
                opciones = self.app.obtener_lista_ciudades()
                self.cb_origen.config(values=opciones, state="readonly")
                self.cb_destino.config(values=opciones, state="readonly")
                self.btn_ejecutar.config(state=tk.NORMAL)
                self.actualizar_grafico(None) # Dibujar el grafo base recién cargado
            else:
                messagebox.showerror("Error", f"No se pudo cargar: {msj}")

    def ejecutar_busqueda(self):
        origen_seleccionado = self.var_origen.get()
        destino_seleccionado = self.var_destino.get()

        if not origen_seleccionado or not destino_seleccionado:
            messagebox.showwarning("Aviso", "Seleccione Origen y Destino.")
            return

        origen_codigo = origen_seleccionado.split(" - ")[0]
        destino_codigo = destino_seleccionado.split(" - ")[0]

        ruta, resultado = self.app.procesar_busqueda(
            origen=origen_codigo,
            destino=destino_codigo,
            tiene_visa=self.var_visa.get(),
            criterio=self.var_criterio.get()
        )

        if ruta is None:
            self.lbl_resultado.config(text=f"❌ Error:\n{resultado}", fg="red")
            self.actualizar_grafico(None)
        else:
            texto = f"✅ ¡Ruta encontrada!\n\n{' ➔ '.join(ruta)}\n\n"
            if self.var_criterio.get() == "costo":
                texto += f"Costo Total: $ {resultado:.2f}"
            else:
                texto += f"Número de Vuelos: {resultado}\n(Escalas: {resultado - 1})"
            
            self.lbl_resultado.config(text=texto, fg="green")
            self.actualizar_grafico(ruta)

    def actualizar_grafico(self, ruta_optima):
        if not GRAFICOS_DISPONIBLES:
            return

        # Limpiar el panel antes de redibujar
        for widget in self.panel_grafico.winfo_children():
            widget.destroy()

        fig = self.app.obtener_figura_mapa(ruta_optima)
        
        # 1. Crear el canvas
        canvas = FigureCanvasTkAgg(fig, master=self.panel_grafico)
        canvas.draw()
        
        # 2. Crear y empaquetar la barra de herramientas interactiva
        toolbar = NavigationToolbar2Tk(canvas, self.panel_grafico)
        toolbar.update()
        
        # 3. Mostrar el canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)