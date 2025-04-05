from pyta4j.analysis.criteria.analysis_criterion import AnalysisCriterion
from pyta4j.core.position import Position
from pyta4j.core.trading_record import TradingRecord

class NumberOfLosingPositionsCriterion(AnalysisCriterion):
    def __init__(self):
        super().__init__()

    def calculate(self, series, arg):
        if isinstance(arg, Position):
            return self.calculate_position(series, arg)
        elif isinstance(arg, TradingRecord):
            return self.calculate_trading_record(series, arg)
        else:
            raise ValueError("Invalid argument type for NumberOfWinningPositionsCriterion.")

    def calculate_position(self, series, position):
        return 1 if position.has_loss() else 0
    
    def calculate_trading_record(self, series, trading_record):
        return sum(1 for pos in trading_record.positions if pos.has_loss())

    def better_than(self, criterion_value1, criterion_value2):
        return criterion_value1 < criterion_value2
