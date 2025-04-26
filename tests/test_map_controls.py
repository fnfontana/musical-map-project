import pytest
from interface.map_controls import add_layer_control
import folium

def test_add_layer_control():
    m = folium.Map(location=[0, 0], zoom_start=2)
    add_layer_control(m)
    # Verifica se LayerControl foi adicionado
    controls = [c for c in m._children.values() if isinstance(c, folium.map.LayerControl)]
    assert len(controls) == 1
