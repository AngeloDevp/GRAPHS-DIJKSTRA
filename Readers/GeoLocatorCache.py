import json
import os
import time
from geopy.geocoders import Nominatim

class GeoLocatorCache:
    def __init__(self, cache_file="data/ciudades_cache.json"):
        self.cache_file = cache_file
        # Nominatim exige un user_agent personalizado para no bloquear tus peticiones
        self.geolocator = Nominatim(user_agent="metro_travel_app_v1")
        # Cargamos la memoria (el JSON) al iniciar la clase
        self.cache = self._load_cache()

    def _load_cache(self):
        """Lee el archivo JSON y lo convierte en un diccionario de Python."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {} # Si el archivo está vacío o corrupto, empezamos de cero
        return {}

    def _save_cache(self):
        """Sobrescribe el archivo JSON con los nuevos datos descubiertos."""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            # indent=4 lo hace legible para humanos si abres el archivo en el bloc de notas
            json.dump(self.cache, f, indent=4)

    def get_coordinates(self, node_code, search_name):
        """
        Devuelve (Longitud, Latitud). 
        node_code: El código corto (ej. 'CCS') para usar como llave en el JSON.
        search_name: El nombre completo (ej. 'Caracas, Venezuela') para buscar en internet.
        """
        # 1. ¿Ya la conocemos? (Lectura instantánea desde el Caché)
        if node_code in self.cache:
            print(f"[Caché] Coordenadas cargadas para {node_code}")
            # El JSON guarda las tuplas como listas [x, y], las devolvemos como tupla (x, y)
            return tuple(self.cache[node_code])

        # 2. No la conocemos. ¡A buscar en Internet!
        print(f"[Internet] Buscando coordenadas para: {search_name}...")
        try:
            location = self.geolocator.geocode(search_name)
            
            if location:
                # IMPORTANTE: Geopy devuelve (Latitud, Longitud)
                # Pero Cartopy necesita (Longitud, Latitud). Así que las invertimos y redondeamos a 2 decimales.
                coords = (round(location.longitude, 2), round(location.latitude, 2))
                
                # Guardamos en nuestra memoria RAM y luego en el disco duro (JSON)
                self.cache[node_code] = coords
                self._save_cache()
                
                print(f" -> ¡Éxito! {node_code} guardado como {coords}")
                
                # REGLA DE ORO DE NOMINATIM: Debes esperar 1 segundo entre cada petición
                # para que sus servidores gratuitos no te baneen la IP.
                time.sleep(1) 
                return coords
            else:
                print(f" -> Error: No se encontró la ubicación de {search_name}")
                return (0, 0) # Fallback para que el programa no colapse
                
        except Exception as e:
            print(f" -> Error de conexión: {e}")
            return (0, 0)