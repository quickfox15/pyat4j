import unittest
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from tests.loaders.csv_trades_loader import CsvTradesLoader
from pyta4j.indicators.sma_indicator import SMAIndicator
from pyta4j.rules.crossed_up_indicator_rule import CrossedUpIndicatorRule

class TestCrossedUpIndicatorRule(unittest.TestCase):
    def setUp(self):
        self.series = CsvTradesLoader.load_bitstamp_series()
        self.close_price = ClosePriceIndicator(self.series)
        self.short_sma = SMAIndicator(self.close_price, 5)
        self.long_sma = SMAIndicator(self.close_price, 30)

        #print first 100 values of short sma and long sma with index
        # for i in range(100):
        #     print(i, self.short_sma.get_value(i), self.long_sma.get_value(i))

    def test_crossed_up_sma(self):
        # Test if short SMA crosses above long SMA at a known index
        rule = CrossedUpIndicatorRule(self.short_sma, self.long_sma)
        # Replace 42 with an index where this happens in TA4J
        self.assertTrue(rule.is_satisfied(10))

    def test_crossed_up_constant(self):
        # Test if close price crosses above 800
        rule = CrossedUpIndicatorRule(self.close_price, 800)
        self.assertTrue(rule.is_satisfied(85))

