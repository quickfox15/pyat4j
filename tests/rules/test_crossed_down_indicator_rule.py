import unittest
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.rules.crossed_down_indicator_rule import CrossedDownIndicatorRule
from tests.loaders.csv_trades_loader import CsvTradesLoader

class TestCrossedDownIndicatorRule(unittest.TestCase):
    def setUp(self):
        self.series = CsvTradesLoader.load_bitstamp_series()
        self.close_price = ClosePriceIndicator(self.series)

    def test_crossed_down_constant(self):
        # Test if close price crosses below 800
        rule = CrossedDownIndicatorRule(self.close_price, 800)
        self.assertTrue(rule.is_satisfied(78, None))