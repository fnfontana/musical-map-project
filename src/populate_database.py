import sqlite3
import csv
import os

# Caminho do banco de dados
DB_PATH = os.path.join('data', 'musical_map.db')

# Caminho da pasta de entrada
INPUT_DIR = os.path.join('input')

def populate_database():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Criar tabela se não existir, agora com restrição UNIQUE
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS musical_styles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT NOT NULL,
            cidade TEXT NOT NULL,
            genero_musical TEXT NOT NULL,
            comentario TEXT,
            UNIQUE(estado, cidade, genero_musical)
        )
        ''')

        # Verificar se a pasta de entrada existe
        if not os.path.exists(INPUT_DIR):
            print(f"A pasta de entrada '{INPUT_DIR}' não existe. Nenhum arquivo para processar.")
            return

        arquivos_processados = 0
        arquivos_com_erro = 0
        # Processar todos os arquivos CSV na pasta de entrada
        for file_name in os.listdir(INPUT_DIR):
            if file_name.endswith('.csv'):
                file_path = os.path.join(INPUT_DIR, file_name)
                print(f"Processando arquivo: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as csvfile:
                        try:
                            reader = csv.DictReader(csvfile)
                            if not set(['estado', 'cidade', 'genero_musical']).issubset(reader.fieldnames):
                                print(f"Erro: Arquivo {file_name} não possui todas as colunas obrigatórias: 'estado', 'cidade', 'genero_musical'.")
                                arquivos_com_erro += 1
                                continue
                            linhas_validas = 0
                            linhas_invalidas = 0
                            for row in reader:
                                if 'estado' in row and 'cidade' in row and 'genero_musical' in row:
                                    try:
                                        cursor.execute('''
                                        INSERT OR IGNORE INTO musical_styles (estado, cidade, genero_musical, comentario)
                                        VALUES (?, ?, ?, ?)
                                        ''', (row['estado'], row['cidade'], row['genero_musical'], row.get('comentario')))
                                        linhas_validas += 1
                                    except Exception as e:
                                        print(f"Erro ao inserir linha no banco de dados: {e} | Linha: {row}")
                                        linhas_invalidas += 1
                                else:
                                    print(f"Linha inválida no arquivo {file_name}: {row}")
                                    linhas_invalidas += 1
                            print(f"Arquivo {file_name}: {linhas_validas} linhas válidas inseridas, {linhas_invalidas} linhas inválidas.")
                            arquivos_processados += 1
                        except csv.Error as e:
                            print(f"Erro ao ler o CSV {file_name}: {e}")
                            arquivos_com_erro += 1
                except Exception as e:
                    print(f"Erro ao abrir o arquivo {file_name}: {e}")
                    arquivos_com_erro += 1

        if arquivos_processados > 0:
            print(f"Processamento concluído: {arquivos_processados} arquivo(s) processado(s) com sucesso.")
        if arquivos_com_erro > 0:
            print(f"Atenção: {arquivos_com_erro} arquivo(s) apresentaram erro e não foram totalmente processados.")
        if arquivos_processados == 0 and arquivos_com_erro == 0:
            print("Nenhum arquivo CSV encontrado para processar.")

        # Salvar alterações e fechar conexão
        conn.commit()
        conn.close()
        print("Banco de dados populado com sucesso!")

    except Exception as e:
        print(f"Erro ao popular o banco de dados: {e}")

if __name__ == "__main__":
    populate_database()