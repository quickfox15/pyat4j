import unittest
import numpy as np
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.indicators.sma_indicator import SMAIndicator
from tests.loaders.csv_trades_loader import CsvTradesLoader
from tests.utils.trading_test_helpers import populate_bar_series

class TestSMAIndicator(unittest.TestCase):
    def setUp(self):
        # Load the trade series once before each test
        self.series = CsvTradesLoader.load_bitstamp_series()
        self.close_price = ClosePriceIndicator(self.series)

    def test_sma_at_index_0(self):
        # At index 0, SMA with a 5-bar window should equal the first close price
        sma = SMAIndicator(self.close_price, 5)
        self.assertAlmostEqual(sma.get_value(0), self.close_price.get_value(0), places=6)

    def test_sma_at_index_4(self):
        # At index 4, SMA should average the first 5 bars (indices 0-4)
        sma = SMAIndicator(self.close_price, 5)
        expected = np.mean([self.close_price.get_value(i) for i in range(0, 5)])
        self.assertAlmostEqual(sma.get_value(4), expected, places=6)

    def test_sma_at_index_42(self):
        # At index 42, SMA should average bars 38-42
        sma = SMAIndicator(self.close_price, 5)
        expected = np.mean([self.close_price.get_value(i) for i in range(38, 43)])
        self.assertAlmostEqual(sma.get_value(42), expected, places=6)

    def test_using_bar_count_3_using_close_price(self):
        prices = [1, 2, 3, 4, 3, 4, 5, 4, 3, 3, 4, 3, 2]
        series = populate_bar_series(prices)
        close_price = ClosePriceIndicator(series);
        indicator = SMAIndicator(close_price, 3)
        self.assertAlmostEqual((1), indicator.get_value(0))
        self.assertAlmostEqual((1.5), indicator.get_value(1))
        self.assertAlmostEqual((2), indicator.get_value(2))
        self.assertAlmostEqual((3), indicator.get_value(3))
        self.assertAlmostEqual((10/3), indicator.get_value(4))
        self.assertAlmostEqual((11/3), indicator.get_value(5))
        self.assertAlmostEqual((4), indicator.get_value(6))
        self.assertAlmostEqual((13/3), indicator.get_value(7))
        self.assertAlmostEqual((4), indicator.get_value(8))
        self.assertAlmostEqual((10/3), indicator.get_value(9))
        self.assertAlmostEqual((10/3), indicator.get_value(10))
        self.assertAlmostEqual((10/3), indicator.get_value(11))
        self.assertAlmostEqual((3), indicator.get_value(12))
