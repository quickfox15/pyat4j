import unittest
from pyta4j.core.trade import TradeType
from pyta4j.core.trading_record import TradingRecord
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.rules.stop_gain_rule import StopGainRule
from tests.utils.trading_test_helpers import populate_bar_series

# Test case for StopGainRule
class TestStopGainRule(unittest.TestCase):
    def setUp(self):
        # Price series from Java test: [100, 105, 110, 120, 150, 120, 160, 180, 170, 135, 104]
        prices = [100, 105, 110, 120, 150, 120, 160, 180, 170, 135, 104]
        series = populate_bar_series(prices)
        self.close_price = ClosePriceIndicator(series)
        self.traded_amount = 1

    def test_is_satisfied_for_buy(self):
        trading_record = TradingRecord(starting_type=TradeType.BUY)
        rule = StopGainRule(self.close_price, 30)  # 30% stop-gain

        # No position initially
        self.assertFalse(rule.is_satisfied(0, None))
        self.assertFalse(rule.is_satisfied(1, trading_record))

        # Enter at index 2 with price 108
        trading_record.enter(2, 108, self.traded_amount)
        self.assertFalse(rule.is_satisfied(2, trading_record))  # Price 110 < 108 * 1.3 = 140.4
        self.assertFalse(rule.is_satisfied(3, trading_record))  # Price 120 < 140.4
        self.assertTrue(rule.is_satisfied(4, trading_record))   # Price 150 > 140.4
        # Exit at index 5
        exit_price = self.close_price.get_value(5)  # 120
        trading_record.exit(5, exit_price, self.traded_amount)

        # Enter at index 5 with price 118
        trading_record.enter(5, 118, self.traded_amount)
        self.assertFalse(rule.is_satisfied(5, trading_record))  # Price 120 < 118 * 1.3 = 153.4
        self.assertTrue(rule.is_satisfied(6, trading_record))   # Price 160 > 153.4
        self.assertTrue(rule.is_satisfied(7, trading_record))   # Price 180 > 153.4

    def test_is_satisfied_for_sell(self):
        trading_record = TradingRecord(starting_type=TradeType.SELL)
        rule = StopGainRule(self.close_price, 10)  # 10% stop-gain

        # No position initially
        self.assertFalse(rule.is_satisfied(0, None))
        self.assertFalse(rule.is_satisfied(1, trading_record))

        # Enter at index 7 with price 178
        trading_record.enter(7, 178, self.traded_amount)
        self.assertFalse(rule.is_satisfied(7, trading_record))  # Price 180 > 178 * 0.9 = 160.2
        self.assertFalse(rule.is_satisfied(8, trading_record))  # Price 170 > 160.2
        self.assertTrue(rule.is_satisfied(9, trading_record))   # Price 135 < 160.2
        # Exit at index 10
        exit_price = self.close_price.get_value(10)  # 104
        trading_record.exit(10, exit_price, self.traded_amount)

        # Enter at index 3 with price 119
        trading_record.enter(3, 119, self.traded_amount)
        self.assertFalse(rule.is_satisfied(3, trading_record))  # Price 120 > 119 * 0.9 = 107.1
        self.assertFalse(rule.is_satisfied(2, trading_record))  # Price 110 > 107.1
        self.assertTrue(rule.is_satisfied(1, trading_record))   # Price 105 < 107.1
        self.assertTrue(rule.is_satisfied(10, trading_record))  # Price 104 < 107.1

if __name__ == '__main__':
    unittest.main()