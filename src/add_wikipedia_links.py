# add_wikipedia_links.py
import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup
import sqlite3
import wikipedia
import os

# Caminho do banco de dados
DB_PATH = os.path.join('data', 'musical_map.db')

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

# Adicionar links da Wikipedia ao banco de dados
def add_wikipedia_links():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Adicionar coluna para links da Wikipedia, se não existir
        cursor.execute('''
        ALTER TABLE musical_styles
        ADD COLUMN wikipedia_link TEXT
        ''')
    except sqlite3.OperationalError:
        # A coluna já existe
        pass

    # Obter gêneros musicais únicos que ainda não têm link
    cursor.execute('SELECT DISTINCT genero_musical FROM musical_styles WHERE wikipedia_link IS NULL OR wikipedia_link = ""')
    genres = cursor.fetchall()

    for genre in genres:
        genre_name = genre[0]
        try:
            # Buscar link da Wikipedia usando a função que pode ser mockada
            link = search_wikipedia_link(genre_name)
            if link:
                cursor.execute('''
                UPDATE musical_styles
                SET wikipedia_link = ?
                WHERE genero_musical = ?
                ''', (link, genre_name))
        except Exception as e:
            print(f"Não foi possível encontrar um link para {genre_name}: {e}")

    # Salvar alterações e fechar conexão
    conn.commit()
    conn.close()
    print("Links da Wikipedia adicionados ao banco de dados com sucesso!")

# Ler gêneros musicais únicos do banco de dados SQLite
def get_genres_from_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT DISTINCT genero_musical FROM musical_styles WHERE genero_musical IS NOT NULL", conn)
    conn.close()
    return df['genero_musical'].dropna().unique()

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Buscar todos os gêneros e seus links atuais
    cursor.execute('SELECT DISTINCT genero_musical, wikipedia_link FROM musical_styles WHERE genero_musical IS NOT NULL')
    genres = cursor.fetchall()
    wikipedia_links = {}
    for genre_name, existing_link in genres:
        if existing_link and str(existing_link).strip():
            print(f"[IGNORADO] '{genre_name}' já possui link: {existing_link}")
            continue
        print(f"[BUSCA] Pesquisando link para: {genre_name}")
        link = search_wikipedia_link(genre_name)
        if link:
            print(f"  Encontrado: {link}")
            wikipedia_links[genre_name] = link
            cursor.execute('''
                UPDATE musical_styles
                SET wikipedia_link = ?
                WHERE genero_musical = ?
            ''', (link, genre_name))
        else:
            print(f"  Não encontrado.")
        time.sleep(2)  # Evita bloqueio do Google
    conn.commit()
    conn.close()
    # Atualizar o HTML inserindo os links
    html_file = "musical_map.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    for genre, link in wikipedia_links.items():
        pattern = rf'(<b>Gênero musical:</b> <span style="color:#2a5599">){re.escape(genre)}(</span>)'
        replacement = rf'\1<a href="{link}" target="_blank">{genre}</a>\2'
        html, n = re.subn(pattern, replacement, html, count=1)
        if n:
            print(f"Link inserido para: {genre}")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Links da Wikipedia inseridos no musical_map.html.")

if __name__ == "__main__":
    add_wikipedia_links()
    main()
