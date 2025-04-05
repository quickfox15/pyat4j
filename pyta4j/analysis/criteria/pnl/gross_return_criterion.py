from pyta4j.analysis.criteria.analysis_criterion import AnalysisCriterion
from pyta4j.core.position import Position

class GrossReturnCriterion(AnalysisCriterion):

    def calculate(self, series, trading_record):

        if isinstance(trading_record, Position):
            return self.calculate_profit(trading_record)
        
        total = 1
        for position in trading_record.get_positions():
            total *= self.calculate_profit(position)
        return total

    def calculate_profit(self, position):
        if position.is_closed():
            return position.get_gross_return()
        return 1

