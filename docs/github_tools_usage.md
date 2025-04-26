# Documentação: Integração com GitHub via github_tools.py

Este documento explica como utilizar o script `dev/github/github_tools.py` para criar issues no GitHub a partir de arquivos YAML.

## Pré-requisitos

- Python instalado (recomenda-se Python 3.8+)
- Biblioteca `requests` instalada (`pip install requests`)
- Token de acesso do GitHub com permissão para criar issues no repositório desejado
- Configuração do arquivo `github_config.yaml` (ver exemplo abaixo)

## Configuração

No diretório `dev/github/`, crie ou edite o arquivo `github_config.yaml` com o seguinte formato:

```yaml
repository: usuario/repositorio
github_token: SEU_TOKEN_AQUI
```

- `repository`: caminho do repositório no formato `usuario/repositorio` (ex: `ffont/musical-map-project`)
- `github_token`: token de acesso pessoal do GitHub

## Estrutura do arquivo YAML para issues

Para criar uma issue, crie um arquivo YAML com o seguinte formato:

```yaml
title: "Título da issue"
body: |
  Descrição detalhada da issue.
labels:
  - bug
  - enhancement
```

- `title`: título da issue
- `body`: descrição detalhada (pode usar múltiplas linhas)
- `labels`: lista de labels a serem atribuídas (opcional)

## Como criar uma issue

No terminal, execute:

```sh
python dev/github/github_tools.py create-issue caminho/para/arquivo_da_issue.yaml
```

Exemplo:

```sh
python dev/github/github_tools.py create-issue dev/github/issue_exemplo.yaml
```

Se tudo estiver correto, a issue será criada no repositório configurado e o link será exibido no terminal.

## Observações

- O script pode ser expandido para outros comandos no futuro.
- Certifique-se de que o token do GitHub tem permissões suficientes.
- Não compartilhe seu token publicamente.
