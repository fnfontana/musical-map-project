import pytest
from interface.markers import add_custom_marker
import folium

def test_add_custom_marker():
    m = folium.Map(location=[0, 0], zoom_start=2)
    marker = add_custom_marker(m, [1, 2], "<b>Teste</b>")
    # Verifica se o marcador foi adicionado ao mapa
    assert marker in m._children.values()
