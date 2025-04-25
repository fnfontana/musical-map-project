import os
import pandas as pd
import sqlite3
import json
from datetime import datetime

# Caminhos dos arquivos (relativos ao diretório raiz do projeto)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'musical_map.db')
CACHE_PATH = os.path.join(BASE_DIR, 'data', 'city_coords_cache.json')
CSV_PATH = os.path.join(BASE_DIR, 'data', 'musical_styles.csv')

def add_columns_if_not_exist(cursor):
    cursor.execute("PRAGMA table_info(musical_styles);")
    columns = [col[1] for col in cursor.fetchall()]
    if 'source' not in columns:
        cursor.execute("ALTER TABLE musical_styles ADD COLUMN source TEXT;")
    if 'last_updated' not in columns:
        cursor.execute("ALTER TABLE musical_styles ADD COLUMN last_updated TIMESTAMP;")
    if 'geocode_cache' not in columns:
        cursor.execute("ALTER TABLE musical_styles ADD COLUMN geocode_cache TEXT;")

def migrate_geocode_cache(conn, cursor):
    with open(CACHE_PATH, 'r', encoding='utf-8') as f:
        cache = json.load(f)
    for city_key, coords in cache.items():
        cidade, estado = city_key.split(', ')
        cursor.execute('''
            UPDATE musical_styles
            SET geocode_cache = ?, latitude = COALESCE(latitude, ?), longitude = COALESCE(longitude, ?)
            WHERE cidade = ? AND estado = ?
        ''', (json.dumps(coords), coords[0], coords[1], cidade, estado))
    conn.commit()

def fill_source_and_last_updated(conn, cursor):
    now = datetime.now().isoformat()
    cursor.execute('''
        UPDATE musical_styles
        SET source = COALESCE(source, 'csv import'),
            last_updated = COALESCE(last_updated, ?)
    ''', (now,))
    conn.commit()

def main():
    # Importar dados do CSV se necessário
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        colunas = {
            'Estado': 'estado',
            'Cidade': 'cidade',
            'Gênero musical': 'genero_musical',
            'Comentário contextual': 'comentario',
        }
        df = df.rename(columns=colunas)
        for col in ['latitude', 'longitude', 'created_at']:
            if col not in df.columns:
                df[col] = None
        conn = sqlite3.connect(DB_PATH)
        df.to_sql('musical_styles', conn, if_exists='append', index=False)
        conn.close()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    add_columns_if_not_exist(cursor)
    migrate_geocode_cache(conn, cursor)
    fill_source_and_last_updated(conn, cursor)
    conn.close()

if __name__ == '__main__':
    main()
