import argparse
import yaml
import os
import requests

# Caminho para o arquivo de configuração do GitHub
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'github_config.yaml')

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def create_issue(yaml_path):
    """Cria uma issue no GitHub a partir de um arquivo YAML."""
    config = load_config()
    with open(yaml_path, 'r', encoding='utf-8') as f:
        issue_data = yaml.safe_load(f)
    url = f"https://api.github.com/repos/{config['repository']}/issues"
    headers = {
        'Authorization': f"token {config['github_token']}",
        'Accept': 'application/vnd.github+json'
    }
    data = {
        'title': issue_data['title'],
        'body': issue_data.get('body', ''),
        'labels': issue_data.get('labels', [])
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print('Issue criada com sucesso:', response.json()['html_url'])
    else:
        print('Falha ao criar issue:', response.status_code, response.text)

def main():
    parser = argparse.ArgumentParser(description='Ferramentas de integração com o GitHub.')
    subparsers = parser.add_subparsers(dest='command')

    # Subcomando para criar issue
    parser_issue = subparsers.add_parser('create-issue', help='Criar uma issue a partir de um arquivo YAML.')
    parser_issue.add_argument('yaml_path', help='Caminho para o arquivo YAML da issue.')

    # Futuramente: adicionar outros subcomandos aqui

    args = parser.parse_args()
    if args.command == 'create-issue':
        create_issue(args.yaml_path)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
