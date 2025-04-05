import unittest

from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.indicators.mma_indicator import MMAIndicator
from tests.utils.trading_test_helpers import populate_bar_series

class TestMMAIndicator(unittest.TestCase):
    
    def test_mma_with_bar_count_3(self):
        prices = [1, 2, 3, 4, 3, 4, 5]
        series = populate_bar_series(prices)
        close = ClosePriceIndicator(series)
        mma = MMAIndicator(close, 3)

        self.assertAlmostEqual((1), mma.get_value(0))
        self.assertAlmostEqual(1.3333333333333333, mma.get_value(1))
        self.assertAlmostEqual(1.8888888888888888, mma.get_value(2))
        self.assertAlmostEqual(2.5925925925925924, mma.get_value(3))
        self.assertAlmostEqual(2.728395061728395, mma.get_value(4))
        self.assertAlmostEqual(3.1522633744855965, mma.get_value(5))
        self.assertAlmostEqual(3.768175582990398, mma.get_value(6))