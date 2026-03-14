import tkinter as tk
from tkinter import ttk, messagebox
from Readers.DataReaderCache import DataReaderCache
from Graph import Graph
from City import City


class CRUDForms:
    def __init__(self, parent, app, updateMapCallback):
        self.parent = parent
        self.app = app 
        self.updateMapCallback = updateMapCallback 
        self.dataReaderCache = DataReaderCache() 

    def GetCities(self):
        return self.app.GetCitiesList()

    def ExtractCityCode(self, selection):
        if not selection: return ""
        return selection.split(" - ")[0].strip()

    def OpenAddCity(self):
        win = tk.Toplevel(self.parent)
        win.title("Añadir Nueva Ciudad")
        win.geometry("300x250") # Un poco más alto para el nuevo combobox
        win.grab_set()

        tk.Label(win, text="Código (Ej. CCS):").pack(pady=(5, 0))
        txt_code = tk.Entry(win)
        txt_code.pack()

        tk.Label(win, text="Nombre (Ej. Caracas):").pack(pady=(5, 0))
        txt_name = tk.Entry(win)
        txt_name.pack()

        tk.Label(win, text="¿Requiere Visa?").pack(pady=(5, 0))
        cb_visa = ttk.Combobox(win, values=["si", "no"], state="readonly", width=20)
        cb_visa.set("no") # Valor por defecto
        cb_visa.pack()

        def save_city():
            code = txt_code.get().strip().upper()
            name = txt_name.get().strip()
            
            requires_visa = True if cb_visa.get() == "si" else False

            if not code or not name:
                messagebox.showerror("Error", "Todos los campos son obligatorios", parent=win)
                return
            
            if code in self.app.graph.cities:
                messagebox.showerror("Error", "El código de ciudad ya existe", parent=win)
                return

            win.config(cursor="watch")
            win.update()

            coords = self.dataReaderCache.GetCoordinates(code, name)
            
            new_city = City(code, name, requires_visa, coords)
            self.app.graph.AddCity(new_city)

            win.config(cursor="")
            self.updateMapCallback() 
            messagebox.showinfo("Éxito", f"Ciudad {name} añadida correctamente.\nEl mapa ha sido actualizado.", parent=win)
            win.destroy()

        tk.Button(win, text="Buscar Coordenadas y Guardar", command=save_city, bg="lightblue").pack(pady=15)

    def OpenDeleteCity(self):
        win = tk.Toplevel(self.parent)
        win.title("Eliminar Ciudad")
        win.geometry("300x150")
        win.grab_set()

        tk.Label(win, text="Seleccione la ciudad a eliminar:").pack(pady=10)
        combo = ttk.Combobox(win, values=self.GetCities(), state="readonly", width=25)
        combo.pack()

        def delete_city():
            code = self.ExtractCityCode(combo.get())
            if not code: return
            
            # Advertencia requerida
            respuesta = messagebox.askyesno("Advertencia", 
                f"¿Está seguro de eliminar {code}?\n¡Todos los vuelos asociados a esta ciudad también desaparecerán!", 
                parent=win)
            
            if respuesta:
                self.app.graph.RemoveCity(code)
                messagebox.showinfo("Éxito", "Ciudad y rutas eliminadas.", parent=win)
                self.updateMapCallback()
                win.destroy()

        tk.Button(win, text="Eliminar", command=delete_city, bg="salmon").pack(pady=15)

    def OpenAddFlight(self):
        win = tk.Toplevel(self.parent)
        win.title("Crear Nuevo Vuelo")
        win.geometry("300x250")
        win.grab_set()

        cities = self.GetCities()

        tk.Label(win, text="Origen:").pack(pady=2)
        cb_origin = ttk.Combobox(win, values=cities, state="readonly", width=25)
        cb_origin.pack()

        tk.Label(win, text="Destino:").pack(pady=2)
        cb_dest = ttk.Combobox(win, values=cities, state="readonly", width=25)
        cb_dest.pack()

        tk.Label(win, text="Costo ($):").pack(pady=2)
        txt_cost = tk.Entry(win)
        txt_cost.pack()

        def save_flight():
            orig = self.ExtractCityCode(cb_origin.get())
            dest = self.ExtractCityCode(cb_dest.get())
            
            if not orig or not dest:
                messagebox.showerror("Error", "Debe seleccionar origen y destino", parent=win)
                return

            if orig == dest:
                messagebox.showerror("Error", "El origen y destino no pueden ser iguales", parent=win)
                return

            try:
                cost = float(txt_cost.get())
                
                # Ejecutamos la función de añadir vuelo
                self.app.graph.AddFlight(orig, dest, cost)
                
                # Inmediatamente ordenamos a la UI que redibuje el grafo
                self.updateMapCallback()
                
                # Mostramos el mensaje (bloquea la ejecución hasta darle OK)
                messagebox.showinfo("Éxito", f"Vuelo de {orig} a {dest} añadido correctamente.\nEl mapa ha sido actualizado.", parent=win)
                
                # Cerramos la ventana modal
                win.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "El costo debe ser un número válido", parent=win)

        tk.Button(win, text="Guardar Vuelo", command=save_flight, bg="lightgreen").pack(pady=15)

    def OpenModifyFlight(self):
        win = tk.Toplevel(self.parent)
        win.title("Modificar Vuelo")
        win.geometry("300x300")
        win.grab_set()

        cities = self.GetCities()

        tk.Label(win, text="Origen:").pack()
        cb_origin = ttk.Combobox(win, values=cities, state="readonly", width=25)
        cb_origin.pack()

        tk.Label(win, text="Destino:").pack()
        cb_dest = ttk.Combobox(win, values=cities, state="readonly", width=25)
        cb_dest.pack()

        # Marco para el costo (oculto inicialmente)
        frame_cost = tk.Frame(win)
        tk.Label(frame_cost, text="Nuevo Costo ($):").pack()
        txt_cost = tk.Entry(frame_cost)
        txt_cost.pack()

        def verify_flight():
            orig = self.ExtractCityCode(cb_origin.get())
            dest = self.ExtractCityCode(cb_dest.get())
            
            if orig and dest in self.app.graph.adjacency.get(orig, {}):
                current_cost = self.app.graph.adjacency[orig][dest]
                txt_cost.delete(0, tk.END)
                txt_cost.insert(0, str(current_cost))
                frame_cost.pack(pady=10) # Mostramos el cuadro de texto
                btn_save.pack()          # Mostramos el botón guardar
                btn_verify.pack_forget() # Ocultamos el botón verificar
            else:
                messagebox.showerror("No Encontrado", "No existe un vuelo directo entre estas ciudades.", parent=win)

        def save_mod():
            orig = self.ExtractCityCode(cb_origin.get())
            dest = self.ExtractCityCode(cb_dest.get())
            try:
                new_cost = float(txt_cost.get())
                self.app.graph.UpdateFlightCost(orig, dest, new_cost)
                messagebox.showinfo("Éxito", "Costo actualizado.", parent=win)
                self.updateMapCallback()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Precio inválido", parent=win)

        btn_verify = tk.Button(win, text="Verificar Existencia", command=verify_flight)
        btn_verify.pack(pady=10)
        
        btn_save = tk.Button(win, text="Guardar Cambios", command=save_mod, bg="lightyellow")

    def OpenDeleteFlight(self):
        win = tk.Toplevel(self.parent)
        win.title("Eliminar Vuelo")
        win.geometry("300x200")
        win.grab_set()

        cities = self.GetCities()

        tk.Label(win, text="Origen:").pack()
        cb_origin = ttk.Combobox(win, values=cities, state="readonly", width=25)
        cb_origin.pack()

        tk.Label(win, text="Destino:").pack()
        cb_dest = ttk.Combobox(win, values=cities, state="readonly", width=25)
        cb_dest.pack()

        def delete_flight():
            orig = self.ExtractCityCode(cb_origin.get())
            dest = self.ExtractCityCode(cb_dest.get())
            
            if orig and dest in self.app.graph.adjacency.get(orig, {}):
                self.app.graph.RemoveFlight(orig, dest)
                messagebox.showinfo("Éxito", "Vuelo eliminado.", parent=win)
                self.updateMapCallback()
                win.destroy()
            else:
                messagebox.showerror("Error", "Ese vuelo no existe.", parent=win)

        tk.Button(win, text="Verificar y Eliminar", command=delete_flight, bg="salmon").pack(pady=15)