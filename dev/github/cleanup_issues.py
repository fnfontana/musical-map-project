from github import Github
import os
import yaml
from collections import defaultdict

def cleanup_duplicate_issues(token, repo_name):
    """
    Remove issues duplicadas, mantendo apenas as mais recentes
    """
    print(f"Iniciando limpeza de issues para {repo_name}")
    
    # Inicializa cliente do GitHub
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # Agrupa issues por título
    issues_by_title = defaultdict(list)
    
    # Lista todas as issues abertas
    print("\nListando issues...")
    for issue in repo.get_issues(state='open'):
        issues_by_title[issue.title].append(issue)
    
    # Para cada grupo de issues com o mesmo título
    total_deleted = 0
    for title, issues in issues_by_title.items():
        if len(issues) > 1:
            # Ordena por data de criação, mais recente primeiro
            sorted_issues = sorted(issues, key=lambda x: x.created_at, reverse=True)
            
            # Mantém a mais recente, deleta as outras
            print(f"\nEncontradas {len(issues)} issues duplicadas para '{title}'")
            print(f"Mantendo issue #{sorted_issues[0].number} (mais recente)")
            
            for issue in sorted_issues[1:]:
                print(f"Deletando issue duplicada #{issue.number}")
                issue.edit(state='closed', state_reason='not_planned')
                total_deleted += 1
    
    print(f"\nLimpeza concluída! {total_deleted} issues duplicadas foram fechadas.")

if __name__ == "__main__":
    config_path = os.path.join("config", "github_config.yaml")
    
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        cleanup_duplicate_issues(
            config["github_token"],
            config["repository"]
        )
    else:
        print("Arquivo de configuração não encontrado.")