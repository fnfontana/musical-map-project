import os
import json
import time
from geopy.geocoders import Nominatim

class CacheManager:
    def __init__(self, cache_path):
        self.cache_path = cache_path

    def get(self, key):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                return cache.get(key)
        return None

    def set(self, key, value):
        cache = {}
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        cache[key] = value
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f)

def get_city_coords(city, state, cache_path):
    cache_manager = CacheManager(cache_path)
    key = f"{city}, {state}"
    cached_coords = cache_manager.get(key)
    if cached_coords:
        return cached_coords
    geolocator = Nominatim(user_agent="musical_map_locator")
    try:
        location = geolocator.geocode(f"{city}, {state}, USA")
        if location:
            coords = [location.latitude, location.longitude]
            cache_manager.set(key, coords)
            time.sleep(1)
            return coords
    except Exception as e:
        print(f"Erro ao geocodificar {city}, {state}: {e}")
    return None
