# Guia de Uso do Musical Map

Este documento explica como instalar, configurar e utilizar o projeto Musical Map.

## Instalação

1. Clone o repositório.
2. Instale as dependências com `pip install -r requirements.txt`.

## Configuração

- Edite `config/settings.yaml` conforme necessário.

## Uso Básico

- Popule o banco: `python src/populate_database.py`
- Gere o mapa: `python src/main.py`
- Adicione links da Wikipedia: `python src/add_wikipedia_links.py`
- Monitore mudanças: `python src/watch_database.py`

## Testes

- Execute todos os testes: `python run_tests.py`

---

> Detalhe comandos e opções avançadas conforme o projeto evoluir.
