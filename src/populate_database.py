import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from monitoring.events import bus
from monitoring.logger import get_logger
from core.database import create_musical_styles_table, insert_musical_style

logger = get_logger(__name__)

# Caminho do banco de dados
DB_PATH = os.path.join('data', 'musical_map.db')

# Caminho da pasta de entrada
INPUT_DIR = os.path.join('input')

def log_event(event_name):
    def handler(*args, **kwargs):
        logger.info(f"[EVENTO] {event_name} - args: {args} kwargs: {kwargs}")
    return handler

bus.subscribe('populate_start', log_event('populate_start'))
bus.subscribe('file_processed', log_event('file_processed'))
bus.subscribe('file_error', log_event('file_error'))
bus.subscribe('populate_success', log_event('populate_success'))
bus.subscribe('populate_error', log_event('populate_error'))

def populate_database():
    try:
        bus.emit('populate_start')
        create_musical_styles_table()

        # Verificar se a pasta de entrada existe
        if not os.path.exists(INPUT_DIR):
            logger.warning(f"A pasta de entrada '{INPUT_DIR}' não existe. Nenhum arquivo para processar.")
            return

        arquivos_processados = 0
        arquivos_com_erro = 0
        # Processar todos os arquivos CSV na pasta de entrada
        for file_name in os.listdir(INPUT_DIR):
            if file_name.endswith('.csv'):
                file_path = os.path.join(INPUT_DIR, file_name)
                logger.info(f"Processando arquivo: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as csvfile:
                        try:
                            reader = csv.DictReader(csvfile)
                            if not set(['estado', 'cidade', 'genero_musical']).issubset(reader.fieldnames):
                                logger.error(f"Erro: Arquivo {file_name} não possui todas as colunas obrigatórias: 'estado', 'cidade', 'genero_musical'.")
                                arquivos_com_erro += 1
                                bus.emit('file_error', file=file_name, reason='colunas ausentes')
                                continue
                            linhas_validas = 0
                            linhas_invalidas = 0
                            for row in reader:
                                if 'estado' in row and 'cidade' in row and 'genero_musical' in row:
                                    try:
                                        insert_musical_style(row['estado'], row['cidade'], row['genero_musical'], row.get('comentario'))
                                        linhas_validas += 1
                                    except Exception as e:
                                        logger.error(f"Erro ao inserir linha no banco de dados: {e} | Linha: {row}")
                                        linhas_invalidas += 1
                                else:
                                    logger.warning(f"Linha inválida no arquivo {file_name}: {row}")
                                    linhas_invalidas += 1
                            logger.info(f"Arquivo {file_name}: {linhas_validas} linhas válidas inseridas, {linhas_invalidas} linhas inválidas.")
                            arquivos_processados += 1
                            bus.emit('file_processed', file=file_name, valid=linhas_validas, invalid=linhas_invalidas)
                        except csv.Error as e:
                            logger.error(f"Erro ao ler o CSV {file_name}: {e}")
                            arquivos_com_erro += 1
                            bus.emit('file_error', file=file_name, reason=str(e))
                except Exception as e:
                    logger.error(f"Erro ao abrir o arquivo {file_name}: {e}")
                    arquivos_com_erro += 1
                    bus.emit('file_error', file=file_name, reason=str(e))

        if arquivos_processados > 0:
            logger.info(f"Processamento concluído: {arquivos_processados} arquivo(s) processado(s) com sucesso.")
        if arquivos_com_erro > 0:
            logger.warning(f"Atenção: {arquivos_com_erro} arquivo(s) apresentaram erro e não foram totalmente processados.")
        if arquivos_processados == 0 and arquivos_com_erro == 0:
            logger.info("Nenhum arquivo CSV encontrado para processar.")

        logger.info("Banco de dados populado com sucesso!")
        bus.emit('populate_success')

    except Exception as e:
        logger.error(f"Erro ao popular o banco de dados: {e}")
        bus.emit('populate_error', error=str(e))

if __name__ == "__main__":
    populate_database()