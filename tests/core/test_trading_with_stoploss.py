import unittest

from pyta4j.core.trade import TradeType
from pyta4j.core.trading_record import TradingRecord


class TestTradingWithStoploss(unittest.TestCase):
    def test_trading_record_and_stop(self):
        # Create a trading record
        record = TradingRecord(starting_type=TradeType.BUY)

        # Enter a position
        record.enter(0, 100, 10)  # Buy 10 units at $100

        # # Define rules
        # stop_loss = StopLossRule(ConstantIndicator(None,95), 5)  # 5% loss
        # stop_gain = StopGainRule(ConstantIndicator(None,109.9), 10)  # 10% gain

        # # Check rules
        # self.assertTrue(stop_loss.is_satisfied(1, record))  # True (90 ≤ 95)
        # # print("stop loss is satisfied ",stop_loss.is_satisfied(1, record))
      
        # self.assertFalse(stop_gain.is_satisfied(1, record))  # False (110 < 110)
        # # print("stop gain is satisfied ",stop_gain.is_satisfied(1, record))

if __name__ == '__main__':
    unittest.main()