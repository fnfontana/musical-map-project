import requests
from monitoring.logger import get_logger

logger = get_logger(__name__)

def search_wikipedia_link(term):
    """
    Busca o link da Wikipedia em inglês usando a API oficial para o termo fornecido.
    """
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": term,
        "utf8": 1
    }
    try:
        resp = requests.get(api_url, params=params)
        data = resp.json()
        search_results = data.get("query", {}).get("search", [])
        if search_results:
            page_title = search_results[0]["title"].replace(' ', '_')
            return f"https://en.wikipedia.org/wiki/{page_title}"
    except Exception as e:
        logger.error(f"Erro ao pesquisar {term}: {e}")
    return None
