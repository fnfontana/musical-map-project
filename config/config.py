"""
Módulo de carregamento centralizado de configurações para o projeto Musical Map.
"""
import os
import yaml
from .defaults import DEFAULTS

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), 'settings.yaml')

def load_settings():
    """Carrega configurações do settings.yaml e mescla com os valores padrão."""
    config = DEFAULTS.copy()
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f) or {}
            config.update({k: v for k, v in user_config.items() if v is not None})
    return config

# Exemplo de uso:
# settings = load_settings()
# print(settings)
