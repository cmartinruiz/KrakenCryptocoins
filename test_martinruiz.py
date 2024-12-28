# -*- coding: utf-8 -*-

import unittest
import pandas as pd
from unittest.mock import patch
from kraken_data import get_top20EUR, fetch_top_coins, date_unix

class TestKrakenAPI(unittest.TestCase):

    def test_get_top20EUR(self):
        """
        Test the `get_top20EUR` function for expected output.
        """
        with patch('kraken_data.get_top20EUR') as mock_get_top20EUR:
            mock_data = pd.DataFrame({
                'Coin': ['BTC', 'ETH'],
                'Price (EUR)': [20000, 1500]
            })
            mock_get_top20EUR.return_value = mock_data
            result = get_top20EUR()
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 2)
            self.assertIn('Coin', result.columns)
            self.assertIn('Price (EUR)', result.columns)
            self.assertTrue(pd.api.types.is_numeric_dtype(result['Price (EUR)']))

    def test_date_unix(self):
        """
        Test the `date_unix` function for correct UNIX conversion.
        """
        date_str = "2023-01-01 00:00:00"
        result = date_unix(date_str)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1672531200)

        # Test for invalid date
        with self.assertRaises(ValueError):
            date_unix("invalid-date")

    def test_fetch_top_coins(self):
        """
        Test the `fetch_top_coins` function for valid DataFrame outputs.
        """
        since_date = date_unix("2023-01-01")
        with patch('kraken_data.fetch_top_coins') as mock_fetch_top_coins:
            mock_1440 = pd.DataFrame({'Coin': ['BTC'], 'Data': [123]})
            mock_60 = pd.DataFrame({'Coin': ['ETH'], 'Data': [456]})
            mock_fetch_top_coins.return_value = (mock_1440, mock_60)
            
            kraken_1440, kraken_60 = fetch_top_coins(since_date)
            self.assertIsInstance(kraken_1440, pd.DataFrame)
            self.assertIsInstance(kraken_60, pd.DataFrame)
            self.assertEqual(len(kraken_1440), 1)
            self.assertEqual(len(kraken_60), 1)

if __name__ == '__main__':
    unittest.main()
