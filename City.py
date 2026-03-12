import csv

class City:
    def __init__(self, code, name, requiresVisa, coordinates=(0.0, 0.0)):
        self.code = code.strip().upper()
        self.name = name.strip()
        self.requiresVisa = requiresVisa
        self.coordinates = coordinates

    def __str__(self):
        return f"{self.code} ({'Visa' if self.requiresVisa else 'Sin Visa'})"