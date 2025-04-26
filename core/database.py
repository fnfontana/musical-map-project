import os
import pandas as pd
import sqlite3

DB_PATH = os.path.join('data', 'musical_map.db')

def get_styles_from_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        style_df = pd.read_sql_query("SELECT * FROM musical_styles", conn)
        conn.close()
        return style_df
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o banco de dados: {e}")

def create_musical_styles_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS musical_styles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estado TEXT NOT NULL,
        cidade TEXT NOT NULL,
        genero_musical TEXT NOT NULL,
        comentario TEXT,
        wikipedia_link TEXT,
        UNIQUE(estado, cidade, genero_musical)
    )
    ''')
    conn.commit()
    conn.close()

def insert_musical_style(estado, cidade, genero_musical, comentario=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO musical_styles (estado, cidade, genero_musical, comentario)
        VALUES (?, ?, ?, ?)
    ''', (estado, cidade, genero_musical, comentario))
    conn.commit()
    conn.close()

def update_wikipedia_link(genero_musical, link):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE musical_styles
        SET wikipedia_link = ?
        WHERE genero_musical = ?
    ''', (link, genero_musical))
    conn.commit()
    conn.close()
