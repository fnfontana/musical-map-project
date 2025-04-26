from interface.filters import apply_genre_filter
import folium

def test_apply_genre_filter_exists():
    m = folium.Map(location=[0, 0], zoom_start=2)
    # Apenas verifica se a função pode ser chamada sem erro
    apply_genre_filter(m, 'Jazz')
