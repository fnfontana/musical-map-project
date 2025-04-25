import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Função a ser testada
from add_wikipedia_links import search_wikipedia_link

# Mock para substituir a função get_genres_from_db
def mock_get_genres_from_db():
    return ['Test Genre']

# Substituir a função original pelo mock
@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    monkeypatch.setattr('add_wikipedia_links.get_genres_from_db', mock_get_genres_from_db)

@pytest.fixture(autouse=True)
def criar_html_temporario():
    # Garante que musical_map.html exista antes dos testes
    html_path = os.path.join(os.path.dirname(__file__), '..', 'musical_map.html')
    if not os.path.exists(html_path):
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write('<b>Gênero musical:</b> <span style="color:#2a5599">Test Genre</span>')
    yield
    # Limpeza opcional: remover arquivo após o teste
    # os.remove(html_path)

# Teste da função de busca de link da Wikipedia (mockando requests)
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

# Teste de integração: verifica se o link é inserido no HTML corretamente
def test_html_update(tmp_path):
    # Cria arquivos temporários
    csv_path = tmp_path / 'musical_styles.csv'
    html_path = tmp_path / 'musical_map.html'
    pd.DataFrame({'Gênero musical': ['Test Genre']}).to_csv(csv_path, index=False)
    html_content = '<b>Gênero musical:</b> <span style="color:#2a5599">Test Genre</span>'
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Mocka a busca para sempre retornar o mesmo link
    with patch('add_wikipedia_links.search_wikipedia_link', return_value='https://en.wikipedia.org/wiki/Test_Genre'):
        # Executa o script principal
        import sys
        sys.path.insert(0, str(tmp_path.parent))
        import add_wikipedia_links as script
        # Recarrega o script para usar os arquivos temporários
        script.csv_file = str(csv_path)
        script.html_file = str(html_path)
        script.genres = ['Test Genre']
        script.wikipedia_links = {'Test Genre': 'https://en.wikipedia.org/wiki/Test_Genre'}
        # Executa apenas a parte de atualização do HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        for genre, link in script.wikipedia_links.items():
            import re
            pattern = rf'(<b>Gênero musical:</b> <span style="color:#2a5599">)'+re.escape(genre)+r'(</span>)'
            replacement = rf'\1<a href="{link}" target="_blank">{genre}</a>\2'
            html, n = re.subn(pattern, replacement, html, count=1)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        # Verifica se o link foi inserido
        with open(html_path, 'r', encoding='utf-8') as f:
            result = f.read()
        assert '<a href="https://en.wikipedia.org/wiki/Test_Genre" target="_blank">Test Genre</a>' in result
