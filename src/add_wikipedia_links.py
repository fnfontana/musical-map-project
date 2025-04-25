# add_wikipedia_links.py
import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup
import sqlite3

# Função para pesquisar o link da Wikipedia em inglês para um termo

def search_wikipedia_link(term):
    # Busca o link da Wikipedia em inglês usando a API oficial
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": term,
        "utf8": 1
    }
    try:
        resp = requests.get(api_url, params=params)
        data = resp.json()
        search_results = data.get("query", {}).get("search", [])
        if search_results:
            page_title = search_results[0]["title"].replace(' ', '_')
            return f"https://en.wikipedia.org/wiki/{page_title}"
    except Exception as e:
        print(f"Erro ao pesquisar {term}: {e}")
    return None

# Ler gêneros musicais únicos do banco de dados SQLite
def get_genres_from_db():
    conn = sqlite3.connect('musical_map.db')
    df = pd.read_sql_query("SELECT DISTINCT genero_musical FROM musical_styles WHERE genero_musical IS NOT NULL", conn)
    conn.close()
    return df['genero_musical'].dropna().unique()

def main():
    genres = get_genres_from_db()

    # Buscar links da Wikipedia para cada gênero
    wikipedia_links = {}
    for genre in genres:
        print(f"Pesquisando link para: {genre}")
        link = search_wikipedia_link(genre)
        if link:
            print(f"  Encontrado: {link}")
            wikipedia_links[genre] = link
        else:
            print(f"  Não encontrado.")
        time.sleep(2)  # Evita bloqueio do Google

    # Atualizar o HTML inserindo os links
    html_file = "musical_map.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    for genre, link in wikipedia_links.items():
        # Substitui apenas a primeira ocorrência de cada gênero musical no HTML
        pattern = rf'(<b>Gênero musical:</b> <span style="color:#2a5599">){re.escape(genre)}(</span>)'
        replacement = rf'\1<a href="{link}" target="_blank">{genre}</a>\2'
        html, n = re.subn(pattern, replacement, html, count=1)
        if n:
            print(f"Link inserido para: {genre}")

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Links da Wikipedia inseridos no musical_map.html.")

if __name__ == "__main__":
    main()
