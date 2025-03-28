import unittest
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.rules.is_falling_rule import IsFallingRule
from tests.utils.trading_test_helpers import populate_bar_series

class TestIsRisingRule(unittest.TestCase):

    def test_is_satisfied(self):
        data = [8, 7, 6, 5, 4, 3, 2, 1, 4, 5]
        series = populate_bar_series(data)
        rule = IsFallingRule(ClosePriceIndicator(series), 3)
        self.assertFalse(rule.is_satisfied(0))
        self.assertFalse(rule.is_satisfied(1))
        self.assertFalse(rule.is_satisfied(2))
        self.assertTrue(rule.is_satisfied(3))
        self.assertTrue(rule.is_satisfied(4))
        self.assertTrue(rule.is_satisfied(5))
        self.assertTrue(rule.is_satisfied(6))
        self.assertTrue(rule.is_satisfied(7))
        self.assertFalse(rule.is_satisfied(8))
        self.assertFalse(rule.is_satisfied(9))
