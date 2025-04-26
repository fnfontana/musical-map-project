def flatten_list(nested_list):
    """Recebe uma lista de listas e retorna uma lista plana."""
    return [item for sublist in nested_list for item in sublist]

def chunk_list(lst, n):
    """Divide uma lista em chunks de tamanho n."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
