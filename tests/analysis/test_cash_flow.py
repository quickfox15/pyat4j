from decimal import Decimal
import unittest
from pyta4j.analysis.cash_flow import CashFlow
from pyta4j.core.trade import Trade, TradeType
from pyta4j.core.trading_record import TradingRecord
from tests.utils.trading_test_helpers import populate_bar_series, populate_trading_record

class TestCashFlow(unittest.TestCase):

    def test_cash_flow_size(self):
        series = populate_bar_series([1.0, 2.0, 3.0, 4.0, 5.0])
        cashFlow = CashFlow(series, TradingRecord(TradeType.BUY))
        self.assertEqual(5, cashFlow.get_size())
        self.assertEqual(1.0, cashFlow.get_value(0))
        self.assertEqual(1.0, cashFlow.get_value(1))
        self.assertEqual(1.0, cashFlow.get_value(2))
        self.assertEqual(1.0, cashFlow.get_value(3))
        self.assertEqual(1.0, cashFlow.get_value(4))

    def test_cash_flow_buy_with_only_one_position(self):
        series = populate_bar_series([1.0, 2.0])
        trading_record = populate_trading_record(TradeType.BUY, [0, 1], series)
        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('2'), cashFlow.get_value(1))

    def test_cash_flow_with_sell_and_buy_trades(self):
        series = populate_bar_series([2.0, 1.0, 3.0, 5.0, 6.0, 3.0, 20.0])
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, 2.0, 1), Trade.sell_at(1, 1.0, 1), Trade.buy_at(3, 5.0, 1),
                  Trade.sell_at(4, 6.0, 1), Trade.sell_at(5, 3.0, 1), Trade.buy_at(6, 20.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(1))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(2))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(3))
        self.assertEqual(Decimal('0.6'), cashFlow.get_value(4))
        self.assertEqual(Decimal('0.6'), cashFlow.get_value(5))
        self.assertEqual(Decimal('-2.8'), cashFlow.get_value(6))


    def test_cash_flow_sell(self):
        series = populate_bar_series([1.0, 2.0, 4.0, 8.0, 16.0, 32.0])
        trading_record = TradingRecord(TradeType.SELL)
        trades = [Trade.sell_at(2, 2.0, 1), Trade.buy_at(3, 4.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('1'), cashFlow.get_value(1))
        self.assertEqual(Decimal('1'), cashFlow.get_value(2))
        self.assertEqual(Decimal('0'), cashFlow.get_value(3))
        self.assertEqual(Decimal('0'), cashFlow.get_value(4))
        self.assertEqual(Decimal('0'), cashFlow.get_value(5))

    def test_cash_flow_short_sell(self):
        series = populate_bar_series([1.0, 2.0, 4.0, 8.0, 16.0, 32.0])
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, 1.0, 1), Trade.sell_at(2, 4.0, 1), Trade.sell_at(2, 4.0, 1),
                  Trade.buy_at(4, 16.0, 1), Trade.buy_at(4, 16.0, 1), Trade.sell_at(5, 32.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('2'), cashFlow.get_value(1))
        self.assertEqual(Decimal('4'), cashFlow.get_value(2))
        self.assertEqual(Decimal('0'), cashFlow.get_value(3))
        self.assertEqual(Decimal('-8'), cashFlow.get_value(4))
        self.assertEqual(Decimal('-8'), cashFlow.get_value(5))


    def test_cash_flow_short_sell_with20_percent_gain(self):
        series = populate_bar_series([110.0, 100.0, 90.0, 80.0])
        trading_record = TradingRecord(TradeType.SELL)
        trades = [Trade.sell_at(1, 100.0, 1), Trade.buy_at(3, 80.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('1'), cashFlow.get_value(1))
        self.assertEqual(Decimal('1.1'), cashFlow.get_value(2))
        self.assertEqual(Decimal('1.2'), cashFlow.get_value(3))


    def test_cash_flow_short_sell_with20_percent_loss(self):
        series = populate_bar_series([90.0, 100.0, 110.0, 120.0])
        trading_record = TradingRecord(TradeType.SELL)
        trades = [Trade.sell_at(1, 100.0, 1), Trade.buy_at(3, 120.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('1'), cashFlow.get_value(1))
        self.assertEqual(Decimal('0.9'), cashFlow.get_value(2))
        self.assertEqual(Decimal('0.8'), cashFlow.get_value(3))

    def test_cash_flow_short_sell_with100_percent_loss(self):
        series = populate_bar_series([90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0])
        trading_record = TradingRecord(TradeType.SELL)
        trades = [Trade.sell_at(1, 100.0, 1), Trade.buy_at(11, 200.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('1'), cashFlow.get_value(1))
        self.assertEqual(Decimal('0.9'), cashFlow.get_value(2))
        self.assertEqual(Decimal('0.8'), cashFlow.get_value(3))
        self.assertEqual(Decimal('0.7'), cashFlow.get_value(4))
        self.assertEqual(Decimal('0.6'), cashFlow.get_value(5))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(6))
        self.assertEqual(Decimal('0.4'), cashFlow.get_value(7))
        self.assertEqual(Decimal('0.3'), cashFlow.get_value(8))
        self.assertEqual(Decimal('0.2'), cashFlow.get_value(9))
        self.assertEqual(Decimal('0.1'), cashFlow.get_value(10))
        self.assertEqual(Decimal('0.0'), cashFlow.get_value(11))

    def test_cash_flow_short_sell_with_over100_percent_loss(self):
        series = populate_bar_series([100.0, 150.0, 200.0, 210.0])
        trading_record = TradingRecord(TradeType.SELL)
        trades = [Trade.sell_at(0, 100.0, 1), Trade.buy_at(3, 210.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(1))
        self.assertEqual(Decimal('0.0'), cashFlow.get_value(2))
        self.assertEqual(Decimal('-0.1'), cashFlow.get_value(3))


    def test_cash_flow_short_sell_big_loss_with_negative_cash_flow(self):
        series = populate_bar_series([3.0, 20.0])
        trading_record = TradingRecord(TradeType.SELL)
        trades = [Trade.sell_at(0, 3.0, 1), Trade.buy_at(1, 20.0, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertAlmostEqual(Decimal('-4.6667'), cashFlow.get_value(1), places=4)


    def test_cash_flow_value(self):
        prices = [3.0, 2.0, 5.0, 1000.0, 5000.0, 0.0001, 4.0, 7.0, 6.0, 7.0, 8.0, 5.0, 6.0]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(2, prices[2], 1), Trade.buy_at(6, prices[6], 1),
                  Trade.sell_at(8, prices[8], 1), Trade.buy_at(9, prices[9], 1), Trade.sell_at(11, prices[11], 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertAlmostEqual(Decimal('2') / Decimal('3'), cashFlow.get_value(1), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3'), cashFlow.get_value(2), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3'), cashFlow.get_value(3), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3'), cashFlow.get_value(4), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3'), cashFlow.get_value(5), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3'), cashFlow.get_value(6), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3') * Decimal('7') / Decimal('4'), cashFlow.get_value(7), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3') * Decimal('6') / Decimal('4'), cashFlow.get_value(8), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3') * Decimal('6') / Decimal('4'), cashFlow.get_value(9), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3') * Decimal('6') / Decimal('4') * Decimal('8') / Decimal('7'),
                           cashFlow.get_value(10), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3') * Decimal('6') / Decimal('4') * Decimal('5') / Decimal('7'),
                           cashFlow.get_value(11), places=4)
        self.assertAlmostEqual(Decimal('5') / Decimal('3') * Decimal('6') / Decimal('4') * Decimal('5') / Decimal('7'),
                           cashFlow.get_value(12), places=4)
       

    def test_really_long_cash_flow(self):
        size = 1000000
        series = populate_bar_series([10] * size)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, 10, 1), Trade.sell_at(size - 1, 10, 1)]
        trading_record.initialize_from_trades(trades)

        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(1, cashFlow.get_value(size - 1))


    def test_cash_flow_with_last_position_open(self):
        prices = [2.0, 1.0, 3.0, 5.0, 6.0, 3.0, 20.0]
        series = populate_bar_series(prices)
        trading_record = TradingRecord(TradeType.BUY)
        trades = [Trade.buy_at(0, prices[0], 1), Trade.sell_at(1, prices[1], 1), Trade.buy_at(3, prices[3], 1),
                  Trade.sell_at(4, prices[4], 1), Trade.sell_at(5, prices[5], 1), Trade.buy_at(6, prices[6], 1)]
        trading_record.initialize_from_trades(trades)
        cashFlow = CashFlow(series, trading_record)
        self.assertEqual(Decimal('1'), cashFlow.get_value(0))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(1))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(2))
        self.assertEqual(Decimal('0.5'), cashFlow.get_value(3))
        self.assertEqual(Decimal('0.6'), cashFlow.get_value(4))
        self.assertEqual(Decimal('0.6'), cashFlow.get_value(5))
        self.assertEqual(Decimal('-2.8'), cashFlow.get_value(6))
        