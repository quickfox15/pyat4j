import unittest
from pyta4j.indicators.helpers.highest_value_Indicator import HighestValueIndicator
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from tests.utils.trading_test_helpers import populate_bar_series

class TestHighstValueIndicator(unittest.TestCase):
    
    def setUp(self):
        prices = [1, 2, 3, 4, 3, 4, 5, 6, 4, 3, 3, 4, 3, 2]
        self.series = populate_bar_series(prices)

    def test_highest_value_using_bar_count_5_using_close_price(self):
        highestValue = HighestValueIndicator(ClosePriceIndicator(self.series), 5)
        self.assertAlmostEqual(4.0, highestValue.get_value(4))
        self.assertAlmostEqual(4.0, highestValue.get_value(5))
        self.assertAlmostEqual(5.0, highestValue.get_value(6))
        self.assertAlmostEqual(6.0, highestValue.get_value(7))
        self.assertAlmostEqual(6.0, highestValue.get_value(8))
        self.assertAlmostEqual(6.0, highestValue.get_value(9))
        self.assertAlmostEqual(6.0, highestValue.get_value(10))
        self.assertAlmostEqual(6.0, highestValue.get_value(11))
        self.assertAlmostEqual(4.0, highestValue.get_value(12))

    def test_first_highest_value_indicator_value_should_be_equals_to_first_data_value(self):
        highestValue = HighestValueIndicator(ClosePriceIndicator(self.series), 5)
        self.assertAlmostEqual(1.0, highestValue.get_value(0))

    def test_highest_value_indicator_when_bar_count_is_greater_than_index(self):
        highestValue = HighestValueIndicator(ClosePriceIndicator(self.series), 500)
        self.assertAlmostEqual(6.0, highestValue.get_value(12))
