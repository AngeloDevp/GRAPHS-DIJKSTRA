
from City import City

cities = {"ALE": City("CCS", "Caracas", True)}
numero = float(5)
for key, city in cities.items():
    print(f"{key}: {city.name}, Visa: {city.requiresVisa}")



if "CCS" not in cities:  # Evitar duplicados
    cities["CCS"] = City("CCS", "Caracas", True)
    print("Ciudad agregada")