# add_wikipedia_links.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import requests
import time
import re
from bs4 import BeautifulSoup
import sqlite3
import wikipedia
from monitoring.events import bus
from core.database import update_wikipedia_link
from monitoring.logger import get_logger

logger = get_logger(__name__)

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
        logger.error(f"Erro ao pesquisar {term}: {e}")
    return None

def log_event(event_name):
    def handler(*args, **kwargs):
        logger.info(f"[EVENTO] {event_name} - args: {args} kwargs: {kwargs}")
    return handler

bus.subscribe('wikipedia_links_start', log_event('wikipedia_links_start'))
bus.subscribe('wikipedia_link_processed', log_event('wikipedia_link_processed'))
bus.subscribe('wikipedia_link_error', log_event('wikipedia_link_error'))
bus.subscribe('wikipedia_links_success', log_event('wikipedia_links_success'))
bus.subscribe('wikipedia_links_error', log_event('wikipedia_links_error'))

# Adicionar links da Wikipedia ao banco de dados
def add_wikipedia_links():
    try:
        bus.emit('wikipedia_links_start')
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
                update_wikipedia_link(genre_name, link)
                bus.emit('wikipedia_link_processed', genre=genre_name, link=link)
            else:
                bus.emit('wikipedia_link_error', genre=genre_name, reason='link não encontrado')
        except Exception as e:
            logger.warning(f"Não foi possível encontrar um link para {genre_name}: {e}")
            bus.emit('wikipedia_link_error', genre=genre_name, reason=str(e))

    # Salvar alterações e fechar conexão
    conn.commit()
    conn.close()
    logger.info("Links da Wikipedia adicionados ao banco de dados com sucesso!")
    bus.emit('wikipedia_links_success')

# Ler gêneros musicais únicos do banco de dados SQLite
def get_genres_from_db():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT DISTINCT genero_musical FROM musical_styles WHERE genero_musical IS NOT NULL", conn)
    conn.close()
    return df['genero_musical'].dropna().unique()

def main():
    try:
        bus.emit('wikipedia_links_start')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Buscar todos os gêneros e seus links atuais
        cursor.execute('SELECT DISTINCT genero_musical, wikipedia_link FROM musical_styles WHERE genero_musical IS NOT NULL')
        genres = cursor.fetchall()
        wikipedia_links = {}
        for genre_name, existing_link in genres:
            if existing_link and str(existing_link).strip():
                logger.info(f"[IGNORADO] '{genre_name}' já possui link: {existing_link}")
                continue
            logger.info(f"[BUSCA] Pesquisando link para: {genre_name}")
            link = search_wikipedia_link(genre_name)
            if link:
                logger.info(f"  Encontrado: {link}")
                wikipedia_links[genre_name] = link
                update_wikipedia_link(genre_name, link)
                bus.emit('wikipedia_link_processed', genre=genre_name, link=link)
            else:
                logger.warning(f"  Não encontrado.")
                bus.emit('wikipedia_link_error', genre=genre_name, reason='link não encontrado')
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
                logger.info(f"Link inserido para: {genre}")
                bus.emit('wikipedia_link_processed', genre=genre, link=link)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info("Links da Wikipedia inseridos no musical_map.html.")
        bus.emit('wikipedia_links_success')
    except Exception as e:
        logger.error(f"Erro ao inserir links no HTML: {e}")
        bus.emit('wikipedia_links_error', error=str(e))

if __name__ == "__main__":
    add_wikipedia_links()
    main()
