"""
Módulo para controles interativos do mapa (camadas, filtros, zoom, etc).
"""

def add_layer_control(folium_map):
    """Adiciona controle de camadas ao mapa Folium."""
    import folium
    folium.LayerControl().add_to(folium_map)

# Futuramente: funções para filtros, busca, customização de visualização, etc.
