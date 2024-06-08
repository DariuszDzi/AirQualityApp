import unittest
import pandas as pd
from app.data_analyzer import analyze_data

class TestDataAnalyzer(unittest.TestCase):

    def test_analyze_data(self):
        data = {
            'date': pd.date_range(start='1/1/2022', periods=5, freq='D'),
            'value': [10, 20, 30, 40, 50]
        }
        df = pd.DataFrame(data)
        result = analyze_data(df)
        self.assertEqual(result['min_value'], 10)
        self.assertEqual(result['max_value'], 50)
        self.assertEqual(result['mean_value'], 30)
        self.assertEqual(result['trend'], 'Increasing')

if __name__ == '__main__':
    unittest.main()
