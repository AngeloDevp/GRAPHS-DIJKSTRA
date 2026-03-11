import csv

class City:
    def __init__(self, code, name, requiresVisa):
        self.code = code.strip().upper()
        self.name = name.strip()
        self.requiresVisa = requiresVisa

    def __str__(self):
        return f"{self.code} ({'Visa' if self.requiresVisa else 'Sin Visa'})"