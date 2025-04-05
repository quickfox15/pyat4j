import unittest

from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.indicators.helpers.gain_indicator import GainIndicator
from tests.utils.trading_test_helpers import populate_bar_series

class TestLossIndicator(unittest.TestCase):

    def test_loss_using_close_price(self):
        prices = [1, 2, 3, 4, 3, 4, 7, 4, 3, 3, 5, 3, 2]
        series = populate_bar_series(prices)
        
        close_price = ClosePriceIndicator(series)
        indicator = GainIndicator(close_price)

        self.assertAlmostEqual((0), indicator.get_value(0))
        self.assertAlmostEqual((1), indicator.get_value(1))
        self.assertAlmostEqual((1), indicator.get_value(2))
        self.assertAlmostEqual((1), indicator.get_value(3))
        self.assertAlmostEqual((0), indicator.get_value(4))
        self.assertAlmostEqual((1), indicator.get_value(5))  
        self.assertAlmostEqual((3), indicator.get_value(6))
        self.assertAlmostEqual((0), indicator.get_value(7))
        self.assertAlmostEqual((0), indicator.get_value(8))
        self.assertAlmostEqual((0), indicator.get_value(9))
        self.assertAlmostEqual((2), indicator.get_value(10))
        self.assertAlmostEqual((0), indicator.get_value(11))
        self.assertAlmostEqual((0), indicator.get_value(12))
