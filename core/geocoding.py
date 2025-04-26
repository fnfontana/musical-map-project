import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from monitoring.logger import get_logger
from utils.cache import CacheManager
import os
import json
import time

logger = get_logger(__name__)

def get_city_coordinates(city, state=None, country='USA', user_agent='musical-map'): 
    """
    Retorna as coordenadas (latitude, longitude) de uma cidade usando o Nominatim.
    """
    geolocator = Nominatim(user_agent=user_agent)
    query = city
    if state:
        query += f', {state}'
    if country:
        query += f', {country}'
    try:
        location = geolocator.geocode(query, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            logger.warning(f'Coordenadas não encontradas para: {query}')
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logger.error(f'Erro de geocodificação para {query}: {e}')
    return None

def get_city_coordinates_with_cache(city, state, cache_path, country='USA', user_agent='musical-map'):
    """
    Busca coordenadas de uma cidade com cache em disco, usando CacheManager.
    """
    cache = CacheManager(cache_path)
    key = f"{city}, {state}"
    coords = cache.get(key)
    if coords:
        return coords
    coords = get_city_coordinates(city, state, country, user_agent)
    if coords:
        cache.set(key, coords)
        time.sleep(1)  # Evita bloqueio do serviço
        return coords
    return None
