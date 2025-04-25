import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from main import style_df, merged

class TestMusicalMap(unittest.TestCase):

    def test_csv_reading(self):
        # Verifica se o DataFrame foi carregado corretamente
        self.assertFalse(style_df.empty, "O arquivo CSV está vazio ou não foi carregado corretamente.")

    def test_columns_exist(self):
        # Garante que as colunas essenciais existem
        expected_columns = {'name', 'Cidade', 'Gênero musical', 'Comentário contextual'}
        self.assertTrue(expected_columns.issubset(set(style_df.columns)), f"Colunas faltando: {expected_columns - set(style_df.columns)}")

    def test_no_null_critical_columns(self):
        # Garante que não há valores nulos em colunas críticas
        critical_columns = ['name', 'Cidade', 'Gênero musical']
        for col in critical_columns:
            self.assertFalse(style_df[col].isnull().any(), f"Coluna crítica '{col}' contém valores nulos.")

    def test_merge_states(self):
        # Verifica se todos os estados presentes no CSV foram associados corretamente no merge
        csv_states = set(style_df['name'].unique())
        merged_states = set(merged[~merged['Gênero musical'].isna()]['name'].unique())
        missing_in_merge = csv_states - merged_states
        self.assertTrue(len(missing_in_merge) == 0, f"Estados do CSV sem associação no merge: {missing_in_merge}")

    def test_no_duplicates_in_merge(self):
        # Garante que não há duplicatas para a combinação de estado, cidade e gênero
        subset = ['name', 'Cidade', 'Gênero musical']
        duplicated = merged[merged.duplicated(subset=subset, keep=False)]
        self.assertTrue(duplicated.empty, f"Existem duplicatas no merge para as colunas {subset}.")

    def test_non_empty_genre(self):
        # Garante que após o filtro de gêneros musicais, ainda há dados
        filtered = merged[~merged['Gênero musical'].isna()]
        self.assertFalse(filtered.empty, "Nenhum dado encontrado após filtrar gêneros musicais.")

if __name__ == "__main__":
    unittest.main()