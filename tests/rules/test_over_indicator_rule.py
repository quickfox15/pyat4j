import unittest

from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.rules.over_indicator_rule import OverIndicatorRule
from tests.utils.trading_test_helpers import populate_bar_series

class TestOverIndicatorRule(unittest.TestCase):

    def test_is_satisfied_number(self):
        data = [20, 15, 10, 5.001, 0.1, 4, 0.2, 100.0001]
        series = populate_bar_series(data)
        rule = OverIndicatorRule(ClosePriceIndicator(series), 5.0)

        self.assertTrue(rule.is_satisfied(0))
        self.assertTrue(rule.is_satisfied(1))
        self.assertTrue(rule.is_satisfied(2))
        self.assertTrue(rule.is_satisfied(3))
        self.assertFalse(rule.is_satisfied(4))
        self.assertFalse(rule.is_satisfied(5))
        self.assertFalse(rule.is_satisfied(6))
        self.assertTrue(rule.is_satisfied(7))

    def test_is_satisfied_indicator(self):
        # Base price data (close prices)
        data1 = [10, 12, 14, 16, 18, 5, 3]
        data2 = [5, 11, 14, 15, 20, 4, 10]

        # Create two BarSeries
        series1 = populate_bar_series(data1)
        series2 = populate_bar_series(data2)

        # Wrap in ClosePriceIndicator
        indicator1 = ClosePriceIndicator(series1)
        indicator2 = ClosePriceIndicator(series2)

        # Use indicator-vs-indicator in OverIndicatorRule
        rule = OverIndicatorRule(indicator1, indicator2)

        # Compare values manually
        expected = [
            True,   # 10 > 5
            True,   # 12 > 11
            False,  # 14 == 14 → not > 
            True,   # 16 > 15
            False,  # 18 < 20
            True,   # 5 > 4
            False   # 3 < 10
        ]

        for i, exp in enumerate(expected):
            self.assertEqual(rule.is_satisfied(i), exp, f"Failed at index {i}")
