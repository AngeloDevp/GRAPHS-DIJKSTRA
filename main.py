from MetroTravelApp import *
from MetroTravelGUI import *
import tkinter as tk

from GUI.MetroTravelGUI2 import MetroTravelGUI2

class Main:
    def run(self):
        app = MetroTravelApp()
        root = tk.Tk()
        # gui = MetroTravelGUI(root, app)
        gui = MetroTravelGUI2(root, app)
        
        root.mainloop()

if __name__ == "__main__":
    programa = Main()
    programa.run()