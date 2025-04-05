import unittest

from pyta4j.indicators.ema_indicator import EMAIndicator
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from tests.utils.trading_test_helpers import populate_bar_series

class TestEMAIndicator(unittest.TestCase):

    def test_using_bar_count_3_using_close_price(self):
        prices = [1, 2, 3, 4, 3, 4, 5, 4, 3, 3, 4, 3, 2]
        series = populate_bar_series(prices)
        
        close_price = ClosePriceIndicator(series)
        indicator = EMAIndicator(close_price, 3)
        
        # Now assert almost equal for each index (using imal values)
        self.assertAlmostEqual((1), indicator.get_value(0))
        self.assertAlmostEqual((1.5), indicator.get_value(1))
        self.assertAlmostEqual((2.25), indicator.get_value(2))
        self.assertAlmostEqual((3.125), indicator.get_value(3))
        self.assertAlmostEqual((3.0625), indicator.get_value(4))
        self.assertAlmostEqual((3.53125), indicator.get_value(5))
        self.assertAlmostEqual((4.265625), indicator.get_value(6))
        self.assertAlmostEqual((4.1328125), indicator.get_value(7))
        self.assertAlmostEqual((3.56640625), indicator.get_value(8))
        self.assertAlmostEqual((3.283203125), indicator.get_value(9))
        self.assertAlmostEqual((3.6416015625), indicator.get_value(10))
        self.assertAlmostEqual((3.32080078125), indicator.get_value(11))
        self.assertAlmostEqual((2.660400390625), indicator.get_value(12))