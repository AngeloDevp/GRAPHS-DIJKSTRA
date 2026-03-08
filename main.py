from MetroTravelApp import *
import tkinter as tk
from tkinter import ttk, messagebox
from MetroTravelGUI import *
class Main:
    def run(self):
        # 1. Creamos la lógica de la App
        app = MetroTravelApp()
        exito = app.inicializar_datos("ciudades.csv", "vuelos.csv")
        
        # 2. Creamos la ventana de Tkinter
        root = tk.Tk()
        
        if not exito:
            messagebox.showerror("Error", "No se encontraron los archivos CSV.")
            root.destroy()
            return
            
        # 3. Le pasamos la App a la GUI para que puedan comunicarse
        gui = MetroTravelGUI(root, app)
        
        # 4. Arrancamos el programa
        root.mainloop()

if __name__ == "__main__":
    programa = Main()
    programa.run()