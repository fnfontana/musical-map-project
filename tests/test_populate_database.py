import sys
import os
import pandas as pd
# Garante que a raiz do projeto está no sys.path para todos os contextos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import shutil
import sqlite3
import pytest
from core.database import get_styles_from_db, create_musical_styles_table, DB_PATH
from src.populate_database import populate_database, INPUT_DIR

def setup_module(module):
    os.makedirs(INPUT_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    create_musical_styles_table()

def teardown_module(module):
    if os.path.exists(INPUT_DIR):
        shutil.rmtree(INPUT_DIR)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_populate_database():
    csv_valido = os.path.join(INPUT_DIR, 'valido.csv')
    csv_invalido = os.path.join(INPUT_DIR, 'invalido.csv')
    with open(csv_valido, 'w', encoding='utf-8') as f:
        f.write('estado,cidade,genero_musical,comentario\n')
        f.write('Texas,Austin,Country,Origem do country moderno\n')
        f.write('California,Los Angeles,Rock,Movimento do rock\n')
    with open(csv_invalido, 'w', encoding='utf-8') as f:
        f.write('estado,cidade,comentario\n')
        f.write('Texas,Austin,Sem genero\n')
    populate_database()
    df = get_styles_from_db()
    assert ('Texas' in df['estado'].values and 'Country' in df['genero_musical'].values)
    assert ('California' in df['estado'].values and 'Rock' in df['genero_musical'].values)
    # O arquivo inválido não deve inserir linhas sem genero_musical
    assert all(pd.notnull(row) for row in df['genero_musical'])
