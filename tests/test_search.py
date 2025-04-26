from interface.search import search_city
import folium

def test_search_city_exists():
    m = folium.Map(location=[0, 0], zoom_start=2)
    # Apenas verifica se a função pode ser chamada sem erro
    search_city(m, 'New York')
