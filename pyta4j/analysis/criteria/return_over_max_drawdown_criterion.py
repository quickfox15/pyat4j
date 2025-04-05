import math
from pyta4j.analysis.criteria.analysis_criterion import AnalysisCriterion
from pyta4j.analysis.criteria.maximum_drawdown_criterion import MaximumDrawdownCriterion
from pyta4j.analysis.criteria.pnl.gross_return_criterion import GrossReturnCriterion

class ReturnOverMaxDrawdownCriterion(AnalysisCriterion):

    def __init__(self):
        self.gross_return_criterion = GrossReturnCriterion()
        self.max_drawdown_criterion = MaximumDrawdownCriterion()

    def calculate(self, series, arg):
        max_drawdown = self.max_drawdown_criterion.calculate(series, arg)
        if max_drawdown == 0:
            return math.nan
        else:
            total_profit = self.gross_return_criterion.calculate(series, arg)
            return total_profit / max_drawdown

    def better_than(self, criterion_value1, criterion_value2):
        return criterion_value1 > criterion_value2
