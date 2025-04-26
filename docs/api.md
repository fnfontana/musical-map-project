# Documentação da API Interna

Este documento descreve as principais funções, classes e módulos do projeto Musical Map.

## Sumário

- [Core](#core)
- [Interface](#interface)
- [Utils](#utils)
- [Configuração](#configuracao)
- [Monitoramento](#monitoramento)

## Core

- `core/database.py`: Funções para manipulação do banco de dados SQLite.
- `core/geocoding.py`: Funções para geocodificação e cache de coordenadas.
- `core/map_generator.py`: Geração do mapa interativo.
- `core/wikipedia_integration.py`: Integração com a Wikipedia.

## Interface

- `interface/map_controls.py`: Controles do mapa (camadas, filtros).
- `interface/markers.py`: Criação e personalização de marcadores.
- `interface/filters.py`: Filtros de visualização.
- `interface/search.py`: Sistema de busca.

## Utils

- `utils/validators.py`: Funções de validação.
- `utils/helpers.py`: Funções auxiliares.
- `utils/cache.py`: Gerenciamento de cache.

## Configuração

- `config/config.py`, `config/defaults.py`, `config/settings.yaml`: Centralização das configurações do projeto.

## Monitoramento

- `monitoring/logger.py`: Logging estruturado.
- `monitoring/events.py`: Sistema de eventos.

---

> Detalhe cada função e classe relevante nos arquivos acima conforme o projeto evoluir.
