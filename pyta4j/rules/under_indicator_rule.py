from decimal import Decimal
from pyta4j.indicators.constant_indicator import ConstantIndicator
from pyta4j.rules.rule import Rule

class UnderIndicatorRule(Rule):
    def __init__(self,first,second):
        super().__init__()
        self.first = first
        if isinstance(second,(int, float, Decimal)):
            self.second  = ConstantIndicator(first.series, second)
        else:
            self.second = second
    
    def is_satisfied(self, index, trading_record=None):
        return self.first.get_value(index) < self.second.get_value(index)