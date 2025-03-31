from pyta4j.indicators.constant_indicator import ConstantIndicator
from pyta4j.indicators.cross_indicator import CrossIndicator
from pyta4j.rules.rule import Rule

class CrossedUpIndicatorRule(Rule):
    def __init__(self, indicator1, indicator2_or_number):

        if isinstance(indicator2_or_number, (int, float)):
            second_arg = ConstantIndicator(indicator2_or_number)
        else:
            second_arg = indicator2_or_number

        self.cross = CrossIndicator( second_arg , indicator1)  # Check if indicator crosses below threshold

    def is_satisfied(self, index, trading_record=None):
        return self.cross.get_value(index)