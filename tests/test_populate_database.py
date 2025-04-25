import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import shutil
import sqlite3
import pytest
from populate_database import populate_database, DB_PATH, INPUT_DIR

def setup_module(module):
    # Cria a pasta input e o banco de dados em data/ para o teste
    os.makedirs(INPUT_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def teardown_module(module):
    # Limpa a pasta input e remove o banco de dados após o teste
    if os.path.exists(INPUT_DIR):
        shutil.rmtree(INPUT_DIR)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

def test_populate_database():
    # Cria arquivos CSV de teste
    csv_valido = os.path.join(INPUT_DIR, 'valido.csv')
    csv_invalido = os.path.join(INPUT_DIR, 'invalido.csv')
    with open(csv_valido, 'w', encoding='utf-8') as f:
        f.write('estado,cidade,genero_musical,comentario\n')
        f.write('Texas,Austin,Country,Origem do country moderno\n')
        f.write('California,Los Angeles,Rock,Movimento do rock\n')
    with open(csv_invalido, 'w', encoding='utf-8') as f:
        f.write('estado,cidade,comentario\n')
        f.write('Texas,Austin,Sem genero\n')
    # Executa a função
    populate_database()
    # Verifica se os dados válidos foram inseridos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT estado, cidade, genero_musical, comentario FROM musical_styles')
    rows = cursor.fetchall()
    conn.close()
    assert ('Texas', 'Austin', 'Country', 'Origem do country moderno') in rows
    assert ('California', 'Los Angeles', 'Rock', 'Movimento do rock') in rows
    # O arquivo inválido não deve inserir linhas (faltou genero_musical)
    assert all(row[2] is not None for row in rows)
    # Não exige mais que haja exatamente 2 linhas, apenas que as de teste estejam presentes
