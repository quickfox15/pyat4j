import math
from pyta4j.indicators.cached_indicator import CachedIndicator
from pyta4j.indicators.statistics.variance_indicator import VarianceIndicator

class StandardDeviationIndicator(CachedIndicator):
    
    def __init__(self, indicator, bar_count):
        super().__init__()
        self.variance = VarianceIndicator(indicator, bar_count)
    
    def calculate(self, index): 
        # Standard deviation is the square root of variance
        variance_value = self.variance.get_value(index)
        if variance_value is None:
            return None
        return math.sqrt(variance_value)
