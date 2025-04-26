import sys
import os
# Garante que a raiz do projeto está no sys.path para todos os contextos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from core.database import get_styles_from_db, insert_musical_style, update_wikipedia_link, create_musical_styles_table, DB_PATH
from add_wikipedia_links import search_wikipedia_link, add_wikipedia_links
import sqlite3

# Mock para substituir a função get_genres_from_db
@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # Setup: cria banco e tabela limpa
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    create_musical_styles_table()
    insert_musical_style('TestState', 'TestCity', 'Test Genre', 'Comentário de teste')
    yield
    # Teardown: remove banco
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_search_wikipedia_link(monkeypatch):
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        def raise_for_status(self):
            pass
        def json(self):
            return {
                "query": {
                    "search": [
                        {"title": "Test Genre"}
                    ]
                }
            }
    def mock_get(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr('requests.get', mock_get)
    link = search_wikipedia_link('Test Genre')
    assert link == 'https://en.wikipedia.org/wiki/Test_Genre'

def test_add_wikipedia_links(monkeypatch):
    monkeypatch.setattr('add_wikipedia_links.search_wikipedia_link', lambda genre: 'https://en.wikipedia.org/wiki/Test_Genre')
    add_wikipedia_links()
    df = get_styles_from_db()
    row = df[df['genero_musical'] == 'Test Genre']
    assert not row.empty
    assert row.iloc[0]['wikipedia_link'] == 'https://en.wikipedia.org/wiki/Test_Genre'
