import pandas as pd
import sqlite3

# Ler dados do CSV
df = pd.read_csv('data/musical_styles.csv')

# Renomear colunas para corresponder ao banco de dados
colunas = {
    'Estado': 'estado',
    'Cidade': 'cidade',
    'Gênero musical': 'genero_musical',
    'Comentário contextual': 'comentario',
}
df = df.rename(columns=colunas)

# Adicionar colunas ausentes se necessário
for col in ['latitude', 'longitude', 'created_at']:
    if col not in df.columns:
        df[col] = None

# Conectar ao banco de dados
conn = sqlite3.connect('musical_map.db')
df.to_sql('musical_styles', conn, if_exists='append', index=False)
conn.close()
