# Musical Map Project

This project visualizes musical styles across the United States using an interactive map. The map is generated using Python and several libraries, including Folium, GeoPandas, and Geopy.

## Features

- **Interactive Map**: Displays musical styles by state and city, with popups containing additional contextual information.
- **Geocoding**: Automatically fetches coordinates for cities and states using the Geopy library.
- **Wikipedia Integration**: Optionally adds Wikipedia links to musical genres for further exploration.
- **Data Caching**: Caches city coordinates to improve performance and reduce API calls.

## Project Structure

- `main.py`: Main script to generate the musical map.
- `add_wikipedia_links.py`: Script to add Wikipedia links to the map.
- `musical_styles.csv`: Input data containing musical styles, states, cities, and contextual comments.
- `musical_map.html`: Output file containing the generated interactive map.
- `city_coords_cache.json`: Cache file for city coordinates.
- `test_add_wikipedia_links.py` and `test_main.py`: Unit tests for the project.

## Requirements

- Python 3.9 or higher
- Libraries: Folium, GeoPandas, Pandas, Geopy

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd musical-map-project
   ```

2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare the `musical_styles.csv` file with the following columns:
   - `Estado`: State name (in Portuguese, e.g., "Nova York").
   - `Cidade`: City name.
   - `Gênero musical`: Musical genre.
   - `Comentário contextual`: Contextual comments.

2. Run the main script to generate the map:

   ```bash
   python main.py
   ```

3. Open the generated `musical_map.html` file in a web browser to view the map.

4. Optionally, add Wikipedia links to the map by following the prompt in the terminal.

## Testing

Run the unit tests to ensure the project works as expected:

```bash
pytest
```

## Notes

- Ensure you have an active internet connection for geocoding and downloading GeoJSON data.
- The project uses a cache (`city_coords_cache.json`) to store city coordinates and reduce API calls.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
