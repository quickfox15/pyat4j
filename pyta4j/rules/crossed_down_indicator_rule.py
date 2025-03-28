
from pyta4j.indicators.constant_indicator import ConstantIndicator
from pyta4j.indicators.cross_indicator import CrossIndicator
from pyta4j.rules.rule import Rule

class CrossedDownIndicatorRule(Rule):
    def __init__(self, indicator, threshold_or_indicator):

        if isinstance(threshold_or_indicator, (int, float)):
            second_arg = ConstantIndicator(indicator.series, threshold_or_indicator)
        else:
            second_arg = threshold_or_indicator

        self.cross = CrossIndicator(indicator, second_arg)  # Check if indicator crosses below threshold

    def is_satisfied(self, index, trading_record):
        return self.cross.get_value(index)