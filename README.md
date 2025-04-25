# Musical Map Project

Projeto que visualiza estilos musicais nos Estados Unidos usando um mapa interativo. O mapa é gerado usando Python e diversas bibliotecas, incluindo Folium, GeoPandas e Geopy.

## Funcionalidades

- **Mapa Interativo**: Exibe estilos musicais por estado e cidade, com popups contendo informações contextuais.
- **Geocodificação**: Busca automática de coordenadas para cidades e estados usando Geopy.
- **Integração Wikipedia**: Adiciona links da Wikipedia para gêneros musicais.
- **Sistema de Cache**: Armazena coordenadas de cidades para melhor performance.
- **Banco de Dados**: Armazenamento persistente em SQLite.
- **Monitoramento**: Sistema de observação de mudanças em tempo real.

## Estrutura do Projeto

```
musical-map-project/
├── src/                    # Código fonte principal
│   ├── main.py            # Script principal do mapa
│   ├── add_wikipedia_links.py  # Integração com Wikipedia
│   ├── populate_database.py    # População do banco de dados
│   └── watch_database.py       # Monitoramento de mudanças
├── tests/                 # Testes unitários e de integração
├── data/                  # Dados e banco SQLite
├── output/                # Arquivos gerados
├── config/                # Arquivos de configuração
├── project/               # Documentação do projeto
└── backup/               # Backup de dados importantes
```

## Documentação

A documentação completa do projeto está organizada no GitHub Projects, dividida em três áreas principais:

- [Sistema Autônomo v2.0](https://github.com/fnfontana/musical-map-project/issues/14)
- [Interface Interativa](https://github.com/fnfontana/musical-map-project/issues/15)
- [Refatoração da Arquitetura](https://github.com/fnfontana/musical-map-project/issues/16)

## Requisitos

- Python 3.9 ou superior
- Bibliotecas: Ver `requirements.txt`
- SQLite 3

## Instalação

1. Clone o repositório:

   ```bash
   git clone <repository-url>
   cd musical-map-project
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Configure o banco de dados:

   ```bash
   python src/populate_database.py
   ```

2. Execute o script principal para gerar o mapa:

   ```bash
   python src/main.py
   ```

3. Abra o arquivo `output/musical_map.html` em um navegador.

4. Opcional: Adicione links da Wikipedia:

   ```bash
   python src/add_wikipedia_links.py
   ```

5. Para monitorar mudanças no banco de dados:

   ```bash
   python src/watch_database.py
   ```

## Testes

Execute os testes unitários:

```bash
pytest
```

## Desenvolvimento

O projeto está em evolução ativa, com foco em:

- Sistema totalmente autônomo
- Interface mais interativa
- Melhor arquitetura e manutenibilidade

## Notas

- Necessária conexão com internet para geocodificação e Wikipedia
- Cache de coordenadas em `data/city_coords_cache.json`
- Backup automático dos dados em `backup/`
- Logs de execução em `output/logs`

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para detalhes.
