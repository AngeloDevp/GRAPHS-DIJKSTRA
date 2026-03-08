import csv

class Ciudad:
    def __init__(self, codigo, nombre, requiere_visa):
        self.codigo = codigo.strip().upper()
        self.nombre = nombre.strip()
        self.requiere_visa = requiere_visa

    def __str__(self):
        return f"{self.codigo} ({'Visa' if self.requiere_visa else 'Sin Visa'})"