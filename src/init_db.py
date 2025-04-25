import sqlite3

def create_tables():
    conn = sqlite3.connect('musical_map.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS musical_styles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT NOT NULL,
            cidade TEXT NOT NULL,
            genero_musical TEXT NOT NULL,
            comentario TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            geocode_cache TEXT
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
