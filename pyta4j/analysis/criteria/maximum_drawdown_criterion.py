from pyta4j.analysis.cash_flow import CashFlow
from pyta4j.analysis.criteria.analysis_criterion import AnalysisCriterion
from pyta4j.core.position import Position
from pyta4j.core.trading_record import TradingRecord

class MaximumDrawdownCriterion(AnalysisCriterion):

    def calculate(self, series, arg):
        if isinstance(arg, Position):
            return self.calculate_position(series, arg)
        elif isinstance(arg, TradingRecord):
            return self.calculate_trading_record(series, arg)
        else:
            raise ValueError("Invalid argument type for MaximumDrawdownCriterion.") 

    def calculate_position(self, series, position):
        if position.is_closed():
            cash_flow = CashFlow(series, position)
            return self.calculate_maximum_drawdown(series, cash_flow)
        return 0

    def calculate_trading_record(self, series, trading_record):
        cash_flow = CashFlow(series, trading_record)
        return self.calculate_maximum_drawdown(series, cash_flow)

    def better_than(self, criterion_value1, criterion_value2):
        return criterion_value1 < criterion_value2
    
    def calculate_maximum_drawdown(self, series, cash_flow):
        maximum_drawdown = 0
        max_peak = 0
        if not series.is_empty():
            for i in range(series.series_begin_index, series.series_end_index + 1):
                value = cash_flow.get_value(i)
                if value > max_peak:
                    max_peak = value

                drawdown = (max_peak - value) / max_peak
                if drawdown > maximum_drawdown:
                    maximum_drawdown = drawdown
        return maximum_drawdown
