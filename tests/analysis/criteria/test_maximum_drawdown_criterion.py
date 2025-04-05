import unittest
from pyta4j.analysis.criteria.maximum_drawdown_criterion import MaximumDrawdownCriterion
from pyta4j.core.trading_record import TradingRecord
from pyta4j.core.trade import Trade, TradeType
from tests.utils.trading_test_helpers import populate_bar_series

class TestMaximumDrawdownCriterion(unittest.TestCase):

    def setUp(self):
        self.criterion = MaximumDrawdownCriterion()

    def test_calculate_with_no_trades(self):
        prices = [1, 2, 3, 6, 5, 20, 3]
        series = populate_bar_series(prices)
        self.assertEqual(0, self.criterion.calculate(series, TradingRecord()))

    def test_calculate_with_only_gains(self):
        prices = [1, 2, 3, 6, 8, 20, 3]
        series = populate_bar_series(prices)
        trading_record = TradingRecord()
        trading_record.enter(0, prices[0], 1)
        trading_record.exit(1, prices[1], 1)
        trading_record.enter(2, prices[2], 1)
        trading_record.exit(5, prices[5], 1)
        self.assertEqual(0, self.criterion.calculate(series, trading_record))

    def test_calculate_with_gains_and_losses(self):
        prices = [1, 2, 3, 6, 5, 20, 3]
        series = populate_bar_series(prices)
        trading_record = TradingRecord()
        trading_record.enter(0, prices[0], 1)
        trading_record.exit(1, prices[1], 1)
        trading_record.enter(3, prices[3], 1)
        trading_record.exit(4, prices[4], 1)
        trading_record.enter(5, prices[5], 1)
        trading_record.exit(6, prices[6], 1)
        self.assertAlmostEqual(.875, self.criterion.calculate(series, trading_record))

    def test_calculate_with_null_series_size(self):
        series = populate_bar_series([])
        self.assertEqual(0, self.criterion.calculate(series, TradingRecord()))


    def test_with_trades_that_sell_before_buying(self):
        prices = [2, 1, 3, 5, 6, 3, 20]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1),
                  Trade.buy_at(3, prices[3], 1), Trade.sell_at(4, prices[4], 1),
                  Trade.sell_at(5, prices[5], 1), Trade.buy_at(6, prices[6], 1)]
        trading_record.initialize_from_trades(trades)
        self.assertAlmostEqual(3.8, self.criterion.calculate(series, trading_record))

    def test_with_simple_trades(self):
        prices = [1, 10, 5, 6, 1]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1),
                  Trade.buy_at(1, prices[1], 1), Trade.sell_at(2, prices[2], 1),
                  Trade.buy_at(2, prices[2], 1), Trade.sell_at(3, prices[3], 1),
                  Trade.buy_at(3, prices[3], 1), Trade.sell_at(4, prices[4], 1)]
        trading_record.initialize_from_trades(trades)
        self.assertAlmostEqual(.9, self.criterion.calculate(series, trading_record))

    def test_better_than(self):
        self.assertTrue(self.criterion.better_than(.9, 1.5))
        self.assertFalse(self.criterion.better_than(1.2, .4))
