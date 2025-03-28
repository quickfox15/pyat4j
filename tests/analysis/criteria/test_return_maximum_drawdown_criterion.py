from decimal import Decimal
import unittest
from pyta4j.analysis.criteria.return_over_max_drawdown_criterion import ReturnOverMaxDrawdownCriterion
from pyta4j.core.trade import Trade, TradeType
from pyta4j.core.trading_record import TradingRecord
from tests.utils.trading_test_helpers import dec, populate_bar_series


class TestReturnOverMaxDrawdownCriterion(unittest.TestCase):

    def setUp(self):
        self.criterion = ReturnOverMaxDrawdownCriterion()

 
    def test_reward_risk_ratio_criterion(self):
        prices = [100, 105, 95, 100, 90, 95, 80, 120]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1),
                  Trade.buy_at(2, prices[2], 1), Trade.sell_at(4, prices[4], 1),
                  Trade.buy_at(5, prices[5], 1), Trade.sell_at(7, prices[7], 1)]
        trading_record.initialize_from_trades(trades)

        total_profit = (105 / 100) * (90 / 95) * (120 / 95)
        peak = (105 / 100) * (100 / 95)
        low = (105 / 100) * (90 / 95) * (80 / 95)

        expected =  Decimal(total_profit / ((peak - low) / peak))
        self.assertAlmostEqual(expected, self.criterion.calculate(series, trading_record))

    def test_reward_risk_ratio_criterion_only_with_gain(self):
        prices = [1, 2, 3, 6, 8, 20, 3]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1),
                  Trade.buy_at(2, prices[2], 1), Trade.sell_at(5, prices[5], 1)]
        trading_record.initialize_from_trades(trades)
        self.assertTrue(self.criterion.calculate(series, trading_record).is_nan())


    def test_reward_risk_ratio_criterion_with_no_positions(self):
        prices = [1, 2, 3, 6, 8, 20, 3]
        series = populate_bar_series(prices)
        self.assertTrue(self.criterion.calculate(series, TradingRecord()).is_nan())

    def test_with_one_position(self):
        prices = [100, 95, 95, 100, 90, 95, 80, 120]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1)]
        trading_record.initialize_from_trades(trades)

        expected = (95 / 100) / ((1 - 0.95))
        self.assertAlmostEqual(dec(expected), self.criterion.calculate(series, trading_record))

    def test_better_than(self):
        self.assertTrue(self.criterion.better_than(dec(3.5), dec(2.2)))
        self.assertFalse(self.criterion.better_than(dec(1.5), dec(2.7)))

    def test_no_draw_down_for_trading_record(self):
        prices = [100, 105, 95, 100, 90, 95, 80, 120]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1),
                  Trade.buy_at(2, prices[2], 1), Trade.sell_at(3, prices[3], 1)]
        trading_record.initialize_from_trades(trades)
        self.assertTrue(self.criterion.calculate(series, trading_record).is_nan())


    def test_no_draw_down_for_position(self):
        prices = [100, 105, 95, 100, 90, 95, 80, 120]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1)]
        trading_record.initialize_from_trades(trades)
        self.assertTrue(self.criterion.calculate(series, trading_record).is_nan())
