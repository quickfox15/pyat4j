import math
import unittest

from pyta4j.indicators.statistics.standard_deviation_indicator import StandardDeviationIndicator
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from tests.utils.trading_test_helpers import populate_bar_series

class TestStandardDeviationIndicator(unittest.TestCase):

    def setUp(self):
        data = [1, 2, 3, 4, 3, 4, 5, 4, 3, 1, 9]
        self.series = populate_bar_series(data)
        
    def test_standard_deviation_using_bar_count_4_using_close_price(self):
        sdv = StandardDeviationIndicator(ClosePriceIndicator(self.series), 4)
        self.assertAlmostEqual((0), sdv.get_value(0))
        self.assertAlmostEqual(math.sqrt(0.25), sdv.get_value(1))
        self.assertAlmostEqual(math.sqrt(2.0 / 3), sdv.get_value(2))
        self.assertAlmostEqual(math.sqrt(1.25), sdv.get_value(3))
        self.assertAlmostEqual(math.sqrt(0.5), sdv.get_value(4))
        self.assertAlmostEqual(math.sqrt(0.25), sdv.get_value(5))
        self.assertAlmostEqual(math.sqrt(0.5), sdv.get_value(6))
        self.assertAlmostEqual(math.sqrt(0.5), sdv.get_value(7))
        self.assertAlmostEqual(math.sqrt(0.5), sdv.get_value(8))

    def test_standard_deviation_should_be_zero_when_bar_count_is_1(self):
        sdv = StandardDeviationIndicator(ClosePriceIndicator(self.series), 1)
        self.assertAlmostEqual(0, sdv.get_value(3))
        self.assertAlmostEqual(0, sdv.get_value(8))
