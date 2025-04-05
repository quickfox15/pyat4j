import unittest

from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.indicators.macd_indicator import MACDIndicator
from tests.utils.trading_test_helpers import populate_bar_series

class TestMACDIndicator(unittest.TestCase):
    
    def setUp(self):
        data = [ 37.08, 36.7, 36.11, 35.85, 35.71, 36.04, 36.41, 37.67, 38.01, 37.79,
                36.83, 37.10, 38.01, 38.50, 38.99]
        self.series = populate_bar_series(data)

    def test_throws_error_on_illegal_arguments(self):
        with self.assertRaises(ValueError):
            MACDIndicator(ClosePriceIndicator(self.series), 10, 5)

    def test_macd_using_period_5_and_10(self):
        macd = MACDIndicator(ClosePriceIndicator(self.series), 5, 10)
        self.assertAlmostEqual((0.0), macd.get_value(0))
        self.assertAlmostEqual((-0.05757), macd.get_value(1),4)
        self.assertAlmostEqual((-0.17488), macd.get_value(2),4)
        self.assertAlmostEqual((-0.26766), macd.get_value(3),4)
        self.assertAlmostEqual((-0.32326), macd.get_value(4),4)
        self.assertAlmostEqual((-0.28399), macd.get_value(5),4)
        self.assertAlmostEqual((-0.18930), macd.get_value(6),4)
        self.assertAlmostEqual((0.06472), macd.get_value(7),4)
        self.assertAlmostEqual((0.25087), macd.get_value(8),4)
        self.assertAlmostEqual((0.30387), macd.get_value(9),4)
        self.assertAlmostEqual((0.16891), macd.get_value(10),4)
        
        self.assertAlmostEqual((36.4098), macd.long_term_ema.get_value(5),4)
        self.assertAlmostEqual((36.1258), macd.short_term_ema.get_value(5),4)
        
        self.assertAlmostEqual((37.0118), macd.long_term_ema.get_value(10),4)
        self.assertAlmostEqual((37.1807), macd.short_term_ema.get_value(10),4)
