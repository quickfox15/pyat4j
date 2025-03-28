import unittest

from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.rules.is_falling_rule import IsRisingRule
from tests.utils.trading_test_helpers import populate_bar_series

class TestIsFallingRule(unittest.TestCase):

    def test_is_satisfied(self):
        data = [8, 7, 6, 5, 4, 1, 2, 4, 5, 6]
        series = populate_bar_series(data)
        rule = IsRisingRule(ClosePriceIndicator(series), 3)
        self.assertFalse(rule.is_satisfied(0))
        self.assertFalse(rule.is_satisfied(1))
        self.assertFalse(rule.is_satisfied(2))
        self.assertFalse(rule.is_satisfied(3))
        self.assertFalse(rule.is_satisfied(4))
        self.assertFalse(rule.is_satisfied(5))
        self.assertFalse(rule.is_satisfied(6))
        self.assertFalse(rule.is_satisfied(7))
        self.assertTrue(rule.is_satisfied(8))
        self.assertTrue(rule.is_satisfied(9))

    def test_is_satisfied_75(self):
        data = [6, 5, 4, 1, 2, 4, 5, 6, 7, 5, 4, 3,2,1]
        series = populate_bar_series(data)
        rule = IsRisingRule(ClosePriceIndicator(series), 4, 0.75)
        self.assertFalse(rule.is_satisfied(0))
        self.assertFalse(rule.is_satisfied(1))
        self.assertFalse(rule.is_satisfied(2))
        self.assertFalse(rule.is_satisfied(3))
        self.assertFalse(rule.is_satisfied(4))
        self.assertFalse(rule.is_satisfied(5))
        self.assertTrue(rule.is_satisfied(6))
        self.assertTrue(rule.is_satisfied(7))
        self.assertTrue(rule.is_satisfied(8))
        self.assertTrue(rule.is_satisfied(9))
        self.assertFalse(rule.is_satisfied(10))
        self.assertFalse(rule.is_satisfied(11))
        self.assertFalse(rule.is_satisfied(12))
        self.assertFalse(rule.is_satisfied(13))
