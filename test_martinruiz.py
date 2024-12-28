# -*- coding: utf-8 -*-

import unittest
import pandas as pd
from kraken_data import get_top20EUR, fetch_top_coins, date_unix

class TestKrakenAPI(unittest.TestCase):

    def test_get_top20EUR(self):
        """
        Test the `get_top20EUR` function for expected output.
        """
        result = get_top20EUR()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 20)  # Ensure it fetches exactly 20 coins
        self.assertIn('Coin', result.columns)
        self.assertIn('Price (EUR)', result.columns)

    def test_date_unix(self):
        """
        Test the `date_unix` function for correct UNIX conversion.
        """
        date_str = "2023-01-01 00:00:00"
        result = date_unix(date_str)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1672531200)  # Check against known UNIX timestamp

    def test_fetch_top_coins(self):
        """
        Test the `fetch_top_coins` function for valid DataFrame outputs.
        """
        since_date = date_unix("2023-01-01")
        kraken_1440, kraken_60 = fetch_top_coins(since_date)
        self.assertIsInstance(kraken_1440, pd.DataFrame)
        self.assertIsInstance(kraken_60, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
