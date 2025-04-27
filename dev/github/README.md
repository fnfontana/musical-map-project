# Automação GitHub - musical-map-project

## Scripts

- `create_ruleset.py`: Cria um ruleset de proteção de branch via API do GitHub.
  - Requer o arquivo `github_config.yaml` com o token e o nome do repositório.
  - Exemplo de uso:
    ```bash
    python create_ruleset.py
    ```

## Configuração

- `github_config.yaml`:
  - `github_token`: Token de acesso pessoal do GitHub (mantenha privado).
  - `repository`: Nome do repositório no formato `usuario/repositorio`.

**Importante:**
- Nunca compartilhe seu token publicamente.
- Recomenda-se adicionar o arquivo github_config.yaml ao .gitignore para evitar vazamento acidental.
