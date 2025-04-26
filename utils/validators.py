import re

def is_valid_url(url: str) -> bool:
    """Valida se uma string é uma URL HTTP(s) válida."""
    regex = re.compile(r'^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$')
    return re.match(regex, url) is not None

def is_nonempty_string(s: str) -> bool:
    """Verifica se a string não é vazia e não contém apenas espaços."""
    return isinstance(s, str) and bool(s.strip())
