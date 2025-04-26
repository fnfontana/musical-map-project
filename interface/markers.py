"""
Módulo para criação e personalização de marcadores do mapa.
"""

def add_custom_marker(folium_map, location, popup_html, icon=None):
    """Adiciona um marcador customizado ao mapa Folium."""
    import folium
    marker = folium.Marker(location=location, popup=folium.Popup(popup_html, max_width=300), icon=icon)
    marker.add_to(folium_map)
    return marker

# Futuramente: funções para ícones por gênero, animações, agrupamento, etc.
