import json
import os
import time
from geopy.geocoders import Nominatim

class DataReaderCache:
    def __init__(self, cacheFileName="data/ciudadesCache.json"):
        self.cacheFileName = cacheFileName
        self.geolocator = Nominatim(user_agent="metro_travel_app_v1")
        self.cache = self.LoadCache()

    def LoadCache(self):
        if os.path.exists(self.cacheFileName):
            try:
                with open(self.cacheFileName, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        return {}

    def SaveCache(self):
        with open(self.cacheFileName, 'w', encoding='utf-8') as file:
            json.dump(self.cache, file, indent=4)

    def GetCoordinates(self, CityCode, SearchName):
        if CityCode in self.cache:
            print(f"[Caché] Coordenadas cargadas para {CityCode}")
            return tuple(self.cache[CityCode])

        print(f"[Internet] Buscando coordenadas para: {SearchName}...")
        try:
            location = self.geolocator.geocode(SearchName)
            
            if location:
                coords = (round(location.longitude, 2), round(location.latitude, 2))
                
                self.cache[CityCode] = coords
                self.SaveCache()
                
                print(f" -> ¡Éxito! {CityCode} guardado como {coords}")
                
                time.sleep(1) 
                return coords
            else:
                print(f" -> Error: No se encontró la ubicación de {SearchName}")
                return (0, 0)
                
        except Exception as e:
            print(f" -> Error de conexión: {e}")
            return (0, 0)