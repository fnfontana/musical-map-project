import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import sqlite3
import pytest
from core.database import (
    create_musical_styles_table,
    insert_musical_style,
    get_styles_from_db,
    update_wikipedia_link,
    DB_PATH
)

def setup_module(module):
    # Remove o banco de dados antes dos testes
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    create_musical_styles_table()

def teardown_module(module):
    # Remove o banco de dados após os testes
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_insert_and_get_styles():
    insert_musical_style('California', 'Los Angeles', 'Rock', 'Movimento do rock')
    insert_musical_style('Texas', 'Austin', 'Country', 'Origem do country moderno')
    df = get_styles_from_db()
    assert not df.empty
    assert 'California' in df['estado'].values
    assert 'Texas' in df['estado'].values
    assert 'Rock' in df['genero_musical'].values
    assert 'Country' in df['genero_musical'].values

def test_update_wikipedia_link():
    insert_musical_style('New York', 'NYC', 'Jazz', 'Berço do jazz')
    update_wikipedia_link('Jazz', 'https://en.wikipedia.org/wiki/Jazz')
    df = get_styles_from_db()
    jazz_row = df[df['genero_musical'] == 'Jazz']
    assert not jazz_row.empty
    assert jazz_row.iloc[0]['wikipedia_link'] == 'https://en.wikipedia.org/wiki/Jazz'
