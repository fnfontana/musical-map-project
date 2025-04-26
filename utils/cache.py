import os
import json
import time
from geopy.geocoders import Nominatim

def get_city_coords(city, state, cache_path):
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            city_coords_cache = json.load(f)
    else:
        city_coords_cache = {}
    key = f"{city}, {state}"
    if key in city_coords_cache:
        return city_coords_cache[key]
    geolocator = Nominatim(user_agent="musical_map_locator")
    try:
        location = geolocator.geocode(f"{city}, {state}, USA")
        if location:
            coords = [location.latitude, location.longitude]
            city_coords_cache[key] = coords
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(city_coords_cache, f)
            time.sleep(1)
            return coords
    except Exception as e:
        print(f"Erro ao geocodificar {city}, {state}: {e}")
    return None
