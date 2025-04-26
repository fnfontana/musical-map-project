import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import folium
import geopandas as gpd
import pandas as pd
from geopy.geocoders import Nominatim
import time
import json
from monitoring.events import bus
from core.database import get_styles_from_db
from core.map_generator import generate_map
from monitoring.logger import get_logger

logger = get_logger(__name__)

def is_test_env():
    # Detecta se está rodando sob pytest
    return ('pytest' in sys.modules) or (os.environ.get('PYTEST_CURRENT_TEST') is not None)

def log_event(event_name):
    def handler(*args, **kwargs):
        logger.info(f"[EVENTO] {event_name} - args: {args} kwargs: {kwargs}")
    return handler

bus.subscribe('start_processing', log_event('start_processing'))
bus.subscribe('data_loaded', log_event('data_loaded'))
bus.subscribe('map_generated', log_event('map_generated'))
bus.subscribe('end_processing', log_event('end_processing'))

bus.emit('start_processing')

DB_PATH = os.path.join('data', 'musical_map.db')
CACHE_PATH = os.path.join('data', 'city_coords_cache.json')
OUTPUT_HTML = os.path.join('output', 'musical_map.html')

# Ler dados do banco de dados SQLite
try:
    style_df = get_styles_from_db()
    if style_df.empty:
        msg = "Erro: o banco de dados está vazio."
        logger.warning(msg)
        if __name__ == "__main__" and not is_test_env():
            exit(1)
        else:
            raise RuntimeError(msg)
    bus.emit('data_loaded', style_df=style_df)
except Exception as e:
    logger.error(e)
    if __name__ == "__main__" and not is_test_env():
        exit(1)
    else:
        raise

# Renomear a coluna 'estado' para 'name' para que o merge funcione corretamente
style_df = style_df.rename(columns={'estado': 'name', 'genero_musical': 'Gênero musical', 'cidade': 'Cidade', 'comentario': 'Comentário contextual'})

# Remover duplicatas antes do merge
style_df = style_df.drop_duplicates(subset=["name", "Cidade", "Gênero musical"])

# Normalizar os nomes dos estados no banco de dados para corresponder aos do GeoJSON
state_name_mapping = {
    "Nova York": "New York",
    "Califórnia": "California",
    "Flórida": "Florida",
    "Geórgia": "Georgia",
    "Havaí": "Hawaii",
    "Luisiana": "Louisiana",
    "Mississípi": "Mississippi",
    "Pensilvânia": "Pennsylvania",
    "Tennessee": "Tennessee",
    "Virgínia": "Virginia",
    "Alasca": "Alaska",
    "Arizona": "Arizona",
    "Arkansas": "Arkansas",
    "Colorado": "Colorado",
    "Connecticut": "Connecticut",
    "Delaware": "Delaware",
    "Distrito de Columbia": "District of Columbia",
    "Idaho": "Idaho",
    "Indiana": "Indiana",
    "Iowa": "Iowa",
    "Kansas": "Kansas",
    "Maine": "Maine",
    "Maryland": "Maryland",
    "Massachusetts": "Massachusetts",
    "Montana": "Montana",
    "Nebraska": "Nebraska",
    "Nevada": "Nevada",
    "Nova Hampshire": "New Hampshire",
    "Nova Jersey": "New Jersey",
    "Novo México": "New Mexico",
    "Carolina do Norte": "North Carolina",
    "Dakota do Norte": "North Dakota",
    "Oregon": "Oregon",
    "Rhode Island": "Rhode Island",
    "Carolina do Sul": "South Carolina",
    "Dakota do Sul": "South Dakota",
    "Utah": "Utah",
    "Vermont": "Vermont",
    "Virgínia Ocidental": "West Virginia",
    "Wisconsin": "Wisconsin",
    "Wyoming": "Wyoming",
    "Porto Rico": "Puerto Rico"
}

style_df['name'] = style_df['name'].replace(state_name_mapping)

# Gerar o mapa interativo
generate_map(style_df, OUTPUT_HTML, CACHE_PATH)
bus.emit('map_generated', output=OUTPUT_HTML)
logger.info(f"Mapa salvo em '{OUTPUT_HTML}'.")

# Perguntar ao usuário se deseja adicionar links da Wikipedia
if not is_test_env():
    resposta = input("Deseja adicionar links da Wikipedia aos gêneros musicais no mapa? (s/n): ").strip().lower()
    if resposta == 's':
        import subprocess
        subprocess.run([sys.executable, os.path.join('src', 'add_wikipedia_links.py')])

bus.emit('end_processing')
