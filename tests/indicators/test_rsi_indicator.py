import unittest

from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.indicators.rsi_indicator import RSIIndicator
from tests.utils.trading_test_helpers import populate_bar_series

class TestRSIIndicator(unittest.TestCase):

    def setUp(self):
        data = [ 50.45, 50.30, 50.20, 50.15, 50.05, 50.06, 50.10, 50.08, 50.03, 50.07, 50.01, 50.14, 50.22, 50.43, 50.50, 50.56, 50.52, 50.70, 50.55, 50.62, 50.90, 50.82, 50.86, 51.20, 51.30,51.10]
        self.series = populate_bar_series(data)

    def test_first_value_should_be_zero(self):
        rsi = RSIIndicator(ClosePriceIndicator(self.series), 14)
        self.assertEqual(0, rsi.get_value(0)) 

    def test_hundred_if_no_loss(self):
        rsi = RSIIndicator(ClosePriceIndicator(self.series), 1)
        self.assertEqual((100), rsi.get_value(14))
        self.assertEqual((100), rsi.get_value(15))

    def test_zero_if_no_gain(self):
        rsi = RSIIndicator(ClosePriceIndicator(self.series), 1)
        self.assertEqual((0), rsi.get_value(1))
        self.assertEqual((0), rsi.get_value(2))

    def test_using_bar_count_14_using_close_price(self):
        rsi = RSIIndicator(ClosePriceIndicator(self.series), 14)
        self.assertAlmostEqual((68.4746), rsi.get_value(15), 3)
        self.assertAlmostEqual((64.7836), rsi.get_value(16), 3)
        self.assertAlmostEqual((72.0776), rsi.get_value(17), 3)
        self.assertAlmostEqual((60.7800), rsi.get_value(18), 3)
        self.assertAlmostEqual((63.6439), rsi.get_value(19), 3)
        self.assertAlmostEqual((72.3433), rsi.get_value(20), 3)
        self.assertAlmostEqual((67.3822), rsi.get_value(21), 3)
        self.assertAlmostEqual((68.5438), rsi.get_value(22), 3)
        self.assertAlmostEqual((76.2770), rsi.get_value(23), 3)
        self.assertAlmostEqual((77.9908), rsi.get_value(24), 3)
        self.assertAlmostEqual((67.4895), rsi.get_value(25), 3)
