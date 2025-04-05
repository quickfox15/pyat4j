import unittest
from pyta4j.core.trade import TradeType
from pyta4j.core.trading_record import TradingRecord
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.rules.stop_loss_rule import StopLossRule
from tests.utils.trading_test_helpers import populate_bar_series

# Test case for StopLossRule
class TestStopLossRule(unittest.TestCase):
    def setUp(self):
        prices = [100, 105, 110, 120, 100, 150, 110, 100]
        series = populate_bar_series(prices)
        self.close_price = ClosePriceIndicator(series)
        self.traded_amount = 1
        self.rule = StopLossRule(self.close_price, 5)  # 5% stop-loss

    def test_is_satisfied_for_buy(self):
        trading_record = TradingRecord(starting_type=TradeType.BUY)

        # No position initially
        self.assertFalse(self.rule.is_satisfied(0, None))
        self.assertFalse(self.rule.is_satisfied(1, trading_record))

        # Enter at index 2 with price 114
        trading_record.enter(2,114, self.traded_amount)
        self.assertFalse(self.rule.is_satisfied(2, trading_record))  # Price 110 > 114 * 0.95 = 108.3
        self.assertFalse(self.rule.is_satisfied(3, trading_record))  # Price 120 > 108.3
        self.assertTrue(self.rule.is_satisfied(4, trading_record))   # Price 100 < 108.3
        # Exit at index 5
        exit_price = self.close_price.get_value(5)  # 150
        trading_record.exit(5, exit_price, self.traded_amount)

        # Enter at index 5 with price 128
        trading_record.enter(5, 128, self.traded_amount)
        self.assertFalse(self.rule.is_satisfied(5, trading_record))  # Price 150 > 128 * 0.95 = 121.6
        self.assertTrue(self.rule.is_satisfied(6, trading_record))   # Price 110 < 121.6
        self.assertTrue(self.rule.is_satisfied(7, trading_record))   # Price 100 < 121.6

    def test_is_satisfied_for_sell(self):
        trading_record = TradingRecord(starting_type=TradeType.SELL)

        # No position initially
        self.assertFalse(self.rule.is_satisfied(0, None))
        self.assertFalse(self.rule.is_satisfied(1, trading_record))

        # Enter at index 1 with price 108
        trading_record.enter(1, 108, self.traded_amount)
        self.assertFalse(self.rule.is_satisfied(1, trading_record))  # Price 105 < 108 * 1.05 = 113.4
        self.assertFalse(self.rule.is_satisfied(2, trading_record))  # Price 110 < 113.4
        self.assertTrue(self.rule.is_satisfied(3, trading_record))   # Price 120 > 113.4
        # Exit at index 4
        exit_price = self.close_price.get_value(4)  # 100
        trading_record.exit(4, exit_price, self.traded_amount)

        # Enter at index 2 with price 114
        trading_record.enter(2, 114, self.traded_amount)
        self.assertFalse(self.rule.is_satisfied(2, trading_record))  # Price 110 < 114 * 1.05 = 119.7
        self.assertTrue(self.rule.is_satisfied(3, trading_record))   # Price 120 > 119.7
        self.assertFalse(self.rule.is_satisfied(4, trading_record))  # Price 100 < 119.7
        self.assertTrue(self.rule.is_satisfied(5, trading_record))   # Price 150 > 119.7

if __name__ == '__main__':
    unittest.main()