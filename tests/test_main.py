import unittest
from main import style_df, merged

class TestMusicalMap(unittest.TestCase):

    def test_csv_reading(self):
        # Verifica se o DataFrame foi carregado corretamente
        self.assertFalse(style_df.empty, "O arquivo CSV está vazio ou não foi carregado corretamente.")

    def test_merge_states(self):
        # Verifica se todos os estados presentes no CSV foram associados corretamente no merge
        csv_states = set(style_df['name'].unique())
        merged_states = set(merged[~merged['Gênero musical'].isna()]['name'].unique())
        missing_in_merge = csv_states - merged_states
        self.assertTrue(len(missing_in_merge) == 0, f"Estados do CSV sem associação no merge: {missing_in_merge}")

if __name__ == "__main__":
    unittest.main()