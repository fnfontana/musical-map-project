import folium
import geopandas as gpd
import pandas as pd
from geopy.geocoders import Nominatim
import time
import os
import json
import sqlite3
import sys

def is_test_env():
    # Detecta se está rodando sob pytest
    return ('pytest' in sys.modules) or (os.environ.get('PYTEST_CURRENT_TEST') is not None)

# Caminhos corretos para arquivos
DB_PATH = os.path.join('data', 'musical_map.db')
CACHE_PATH = os.path.join('data', 'city_coords_cache.json')
OUTPUT_HTML = os.path.join('output', 'musical_map.html')

# Ler dados do banco de dados SQLite
try:
    conn = sqlite3.connect(DB_PATH)
    style_df = pd.read_sql_query("SELECT * FROM musical_styles", conn)
    conn.close()
    if style_df.empty:
        print("Erro: o banco de dados está vazio.")
        exit(1)
except Exception as e:
    print(f"Erro ao ler o banco de dados: {e}")
    exit(1)

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

url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
states = gpd.read_file(url)

# Mesclar os dados geográficos com os dados musicais usando a coluna 'name'
merged = states.merge(style_df, on="name", how="left")

# Garantir que o GeoDataFrame esteja no sistema de coordenadas correto (WGS84)
if merged.crs is None or merged.crs.to_string() != 'EPSG:4326':
    merged = merged.to_crs('EPSG:4326')

# Identificar estados que ainda estão sem dados após o merge
missing_states = merged[merged['Gênero musical'].isna()]
print("Estados sem dados musicais após o merge:", missing_states['name'].tolist())

# Criar o mapa centralizado nos EUA
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles=None)

# Adicionar camada de tiles estilo Google Maps
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Maps',
    overlay=False,
    control=True
).add_to(m)

# Função para obter coordenadas de uma cidade e estado
geolocator = Nominatim(user_agent="musical_map_locator")
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, 'r', encoding='utf-8') as f:
        city_coords_cache = json.load(f)
else:
    city_coords_cache = {}

def get_city_coords(city, state):
    key = f"{city}, {state}"
    if key in city_coords_cache:
        return city_coords_cache[key]
    # Só busca se não existir no cache
    try:
        location = geolocator.geocode(f"{city}, {state}, USA")
        if location:
            coords = [location.latitude, location.longitude]
            city_coords_cache[key] = coords
            with open(CACHE_PATH, 'w', encoding='utf-8') as f:
                json.dump(city_coords_cache, f)
            time.sleep(1)  # Evita sobrecarga na API
            return coords
    except Exception as e:
        print(f"Erro ao geocodificar {city}, {state}: {e}")
    return None

# Adicionar marcadores: para cada estado, se houver dados, posicionar o marcador no centroide
for idx, row in merged.iterrows():
    if pd.notna(row['Gênero musical']):
        coords = get_city_coords(row['Cidade'], row['name'])
        if coords:
            lat, lon = coords
        else:
            centroid = row['geometry'].centroid
            lat, lon = centroid.y, centroid.x
        # HTML customizado para o popup
        popup_html = f'''
        <div style="width: 260px; font-size: 15px;">
            <b>Gênero musical:</b> <span style="color:#2a5599">{row['Gênero musical']}</span><br>
            <b>Cidade:</b> <i>{row['Cidade']}</i><br>
            <b>Comentário:</b><br>
            <span style="font-size: 14px; color: #444;">{row['Comentário contextual']}</span>
        </div>
        '''
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)

# Adicionar controle de camadas
folium.LayerControl().add_to(m)

# Salvar o mapa interativo em um arquivo HTML
m.save(OUTPUT_HTML)
print(f"Mapa salvo em '{OUTPUT_HTML}'.")

# Perguntar ao usuário se deseja adicionar links da Wikipedia
if not is_test_env():
    resposta = input("Deseja adicionar links da Wikipedia aos gêneros musicais no mapa? (s/n): ").strip().lower()
    if resposta == 's':
        import subprocess
        subprocess.run(['python', 'src/add_wikipedia_links.py'])
