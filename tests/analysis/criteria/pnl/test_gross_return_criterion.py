import unittest
from decimal import Decimal
from pyta4j.analysis.criteria.pnl.gross_return_criterion import GrossReturnCriterion
from pyta4j.core.trade import TradeType
from pyta4j.core.trading_record import TradingRecord
from pyta4j.core.position import Position
from tests.utils.trading_test_helpers import populate_bar_series, populate_trading_record

class TestGrossReturnCriterion(unittest.TestCase):

    def setUp(self):
        self.criterion = GrossReturnCriterion()

    def test_calculate_with_winning_long_positions(self):
        series = populate_bar_series([100, 105, 110, 100, 95, 105])
        trading_record = populate_trading_record(TradeType.BUY, [0,2,3,5], series)
        # Expected: (110/100) * (105/100) = 1.10 * 1.05
        expected = Decimal('1.10') * Decimal('1.05')
        result = self.criterion.calculate(series, trading_record)
        self.assertAlmostEqual(float(expected), float(result), places=10)

    def test_calculate_with_losing_long_positions(self):
        prices = [100, 95, 100, 80, 85, 70]
        series = populate_bar_series(prices)
        trading_record = populate_trading_record(TradeType.BUY, [0,1,2,5], series)
        # Expected: (95/100) * (70/100) = 0.95 * 0.7
        expected = Decimal('0.95') * Decimal('0.7')
        result = self.criterion.calculate(series, trading_record)
        self.assertAlmostEqual(float(expected), float(result), places=10)

    def test_calculate_return_with_winning_short_positions(self):
   
        series = populate_bar_series([100, 95, 100, 80, 85, 70])
        trading_record = populate_trading_record(TradeType.SELL, [0,1,2,5], series)
        # Expected: (100/95) * (100/70) ≈ 1.05 * 1.30
        expected = Decimal('1.05') * Decimal('1.30')
        result = self.criterion.calculate(series, trading_record)
        self.assertAlmostEqual(float(expected), float(result), places=10)
    
    def test_calculate_return_with_losing_short_positions(self):
        series = populate_bar_series([100, 105, 100, 80, 85, 130])
        trading_record = populate_trading_record(TradeType.SELL, [0,1,2,5], series)
        # Expected: (100/105) * (100/130) ≈ 0.95 * 0.70
        expected = Decimal('0.95') * Decimal('0.70')
        result = self.criterion.calculate(series, trading_record)
        self.assertAlmostEqual(float(expected), float(result), places=10)

    def test_calculate_with_no_positions_should_return_1(self):
        series = populate_bar_series([100, 95, 100, 80, 85, 70])
        trading_record = TradingRecord(TradeType.BUY)
        result = self.criterion.calculate(series, trading_record)
        self.assertAlmostEqual(1.0, float(result), places=10)
    
    def test_calculate_with_opened_position_should_return_1(self):
        series = populate_bar_series([100, 95, 100, 80, 85, 70])
        position = Position()
        result = self.criterion.calculate(series, position)
        self.assertAlmostEqual(1.0, float(result), places=10)
        position.operate(0,Decimal('NaN'),Decimal('NaN'))  # Open a position
        result = self.criterion.calculate(series, position)
        self.assertAlmostEqual(1.0, float(result), places=10)

    def test_calculate_one_open_position_should_return_one(self):
        series = populate_bar_series([100, 95])
        trading_record = populate_trading_record(TradeType.BUY, [0], series)
        result = self.criterion.calculate(series, trading_record)
        self.assertAlmostEqual(1.0, float(result), places=10)