import requests
import yaml
import os

# Caminhos dos arquivos
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'github_config.yaml')
RULESET_PATH = os.path.join(os.path.dirname(__file__), 'master_ruleset.json')

# Carregar configurações do GitHub
def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config['github_token'].strip('"'), config['repository']

# Carregar JSON do ruleset
def load_ruleset():
    with open(RULESET_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    token, repo = load_config()
    url = f'https://api.github.com/repos/{repo}/rulesets'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    data = load_ruleset()
    response = requests.post(url, headers=headers, data=data)
    print(f'Status: {response.status_code}')
    try:
        print(response.json())
    except Exception:
        print(response.text)

if __name__ == '__main__':
    main()
