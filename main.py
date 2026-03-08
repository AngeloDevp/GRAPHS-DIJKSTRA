from MetroTravelApp import *
from MetroTravelGUI import *
import tkinter as tk

class Main:
    def run(self):
        app = MetroTravelApp()
        root = tk.Tk()
        gui = MetroTravelGUI(root, app)
        root.mainloop()

if __name__ == "__main__":
    programa = Main()
    programa.run()