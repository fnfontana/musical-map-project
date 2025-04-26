import unittest
import sys
import os
import sqlite3
from core.database import get_styles_from_db
from core.map_generator import generate_map

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Garante que o banco de dados e a tabela existem e insere dados de teste antes dos testes
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/musical_map.db'))
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS musical_styles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estado TEXT NOT NULL,
        cidade TEXT NOT NULL,
        genero_musical TEXT NOT NULL,
        comentario TEXT
    )
''')
cursor.execute('SELECT COUNT(*) FROM musical_styles')
if cursor.fetchone()[0] == 0:
    cursor.execute('''
        INSERT INTO musical_styles (estado, cidade, genero_musical, comentario)
        VALUES ('California', 'Los Angeles', 'Rock', 'Movimento do rock'),
               ('Texas', 'Austin', 'Country', 'Origem do country moderno')
    ''')
conn.commit()
conn.close()

style_df = get_styles_from_db()
# Simula o processamento feito no main.py
style_df = style_df.rename(columns={'estado': 'name', 'genero_musical': 'Gênero musical', 'cidade': 'Cidade', 'comentario': 'Comentário contextual'})
style_df = style_df.drop_duplicates(subset=["name", "Cidade", "Gênero musical"])

import geopandas as gpd
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
merged = states.merge(style_df, on="name", how="left")
if merged.crs is None or merged.crs.to_string() != 'EPSG:4326':
    merged = merged.to_crs('EPSG:4326')

class TestMusicalMap(unittest.TestCase):
    def test_csv_reading(self):
        self.assertFalse(style_df.empty, "O arquivo CSV está vazio ou não foi carregado corretamente.")
    def test_columns_exist(self):
        expected_columns = {'name', 'Cidade', 'Gênero musical', 'Comentário contextual'}
        self.assertTrue(expected_columns.issubset(set(style_df.columns)), f"Colunas faltando: {expected_columns - set(style_df.columns)}")
    def test_no_null_critical_columns(self):
        critical_columns = ['name', 'Cidade', 'Gênero musical']
        for col in critical_columns:
            self.assertFalse(style_df[col].isnull().any(), f"Coluna crítica '{col}' contém valores nulos.")
    def test_merge_states(self):
        csv_states = set(style_df['name'].unique())
        merged_states = set(merged[~merged['Gênero musical'].isna()]['name'].unique())
        missing_in_merge = csv_states - merged_states
        self.assertTrue(len(missing_in_merge) == 0, f"Estados do CSV sem associação no merge: {missing_in_merge}")
    def test_no_duplicates_in_merge(self):
        subset = ['name', 'Cidade', 'Gênero musical']
        duplicated = merged[merged.duplicated(subset=subset, keep=False)]
        self.assertTrue(duplicated.empty, f"Existem duplicatas no merge para as colunas {subset}.")
    def test_non_empty_genre(self):
        filtered = merged[~merged['Gênero musical'].isna()]
        self.assertFalse(filtered.empty, "Nenhum dado encontrado após filtrar gêneros musicais.")

if __name__ == "__main__":
    unittest.main()