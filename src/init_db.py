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
            latitude REAL,
            longitude REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
