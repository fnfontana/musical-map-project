import folium
import geopandas as gpd
import pandas as pd
import os
import json
import time
from geopy.geocoders import Nominatim
from core.geocoding import get_city_coordinates_with_cache
from core.database import get_styles_from_db
from interface.map_controls import add_layer_control
from interface.markers import add_custom_marker
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_map(style_df, output_html, cache_path):
    # Renomear colunas para merge
    style_df = style_df.rename(columns={'estado': 'name', 'genero_musical': 'Gênero musical', 'cidade': 'Cidade', 'comentario': 'Comentário contextual'})
    style_df = style_df.drop_duplicates(subset=["name", "Cidade", "Gênero musical"])
    state_name_mapping = {
        "Nova York": "New York", "Califórnia": "California", "Flórida": "Florida", "Geórgia": "Georgia", "Havaí": "Hawaii", "Luisiana": "Louisiana", "Mississípi": "Mississippi", "Pensilvânia": "Pennsylvania", "Tennessee": "Tennessee", "Virgínia": "Virginia", "Alasca": "Alaska", "Arizona": "Arizona", "Arkansas": "Arkansas", "Colorado": "Colorado", "Connecticut": "Connecticut", "Delaware": "Delaware", "Distrito de Columbia": "District of Columbia", "Idaho": "Idaho", "Indiana": "Indiana", "Iowa": "Iowa", "Kansas": "Kansas", "Maine": "Maine", "Maryland": "Maryland", "Massachusetts": "Massachusetts", "Montana": "Montana", "Nebraska": "Nebraska", "Nevada": "Nevada", "Nova Hampshire": "New Hampshire", "Nova Jersey": "New Jersey", "Novo México": "New Mexico", "Carolina do Norte": "North Carolina", "Dakota do Norte": "North Dakota", "Oregon": "Oregon", "Rhode Island": "Rhode Island", "Carolina do Sul": "South Carolina", "Dakota do Sul": "South Dakota", "Utah": "Utah", "Vermont": "Vermont", "Virgínia Ocidental": "West Virginia", "Wisconsin": "Wisconsin", "Wyoming": "Wyoming", "Porto Rico": "Puerto Rico"
    }
    style_df['name'] = style_df['name'].replace(state_name_mapping)
    url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    states = gpd.read_file(url)
    merged = states.merge(style_df, on="name", how="left")
    if merged.crs is None or merged.crs.to_string() != 'EPSG:4326':
        merged = merged.to_crs('EPSG:4326')
    missing_states = merged[merged['Gênero musical'].isna()]
    logger.warning("Estados sem dados musicais após o merge: %s", missing_states['name'].tolist())
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles=None)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps',
        overlay=False,
        control=True
    ).add_to(m)
    geolocator = Nominatim(user_agent="musical_map_locator")
    for idx, row in merged.iterrows():
        if pd.notna(row['Gênero musical']):
            coords = get_city_coordinates_with_cache(row['Cidade'], row['name'], cache_path)
            if coords:
                lat, lon = coords
            else:
                centroid = row['geometry'].centroid
                lat, lon = centroid.y, centroid.x
            # Adiciona link da Wikipedia se existir
            wikipedia_link = row.get('wikipedia_link')
            if wikipedia_link and isinstance(wikipedia_link, str) and wikipedia_link.strip():
                genero_html = f'<a href="{wikipedia_link}" target="_blank">{row["Gênero musical"]}</a>'
            else:
                genero_html = f'<span style="color:#2a5599">{row["Gênero musical"]}</span>'
            popup_html = f'''
            <div style="width: 260px; font-size: 15px;">
                <b>Gênero musical:</b> {genero_html}<br>
                <b>Cidade:</b> <i>{row['Cidade']}</i><br>
                <b>Comentário:</b><br>
                <span style="font-size: 14px; color: #444;">{row['Comentário contextual']}</span>
            </div>
            '''
            add_custom_marker(m, [lat, lon], popup_html)
    add_layer_control(m)
    m.save(output_html)
    logger.info("Mapa salvo em '%s'.", output_html)
