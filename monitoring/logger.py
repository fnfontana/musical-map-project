"""
Módulo de logging estruturado para o projeto Musical Map.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'musical_map.log')

# Corrige erro caso 'logs' exista como arquivo
if os.path.exists(LOG_DIR) and not os.path.isdir(LOG_DIR):
    os.remove(LOG_DIR)

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Configuração básica do logger raiz
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        RotatingFileHandler(LOG_FILE, maxBytes=2*1024*1024, backupCount=5, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def get_logger(name: str) -> logging.Logger:
    """Obtém um logger configurado para o projeto."""
    return logging.getLogger(name)

# Exemplo de uso:
# logger = get_logger(__name__)
# logger.info('Mensagem de teste')
