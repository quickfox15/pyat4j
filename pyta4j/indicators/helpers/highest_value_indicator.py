import math
from pyta4j.indicators.cached_indicator import CachedIndicator

class HighestValueIndicator(CachedIndicator):
    def __init__(self, indicator, bar_count):
        super().__init__()
        self.indicator = indicator
        self.bar_count = bar_count

    def calculate(self, index):
        if math.isnan(self.indicator.get_value(index)) and self.bar_count != 1:
            return HighestValueIndicator(self.indicator, self.bar_count - 1).get_value(index - 1)
        
        end = max(0, index - self.bar_count + 1)
        highest = self.indicator.get_value(index)

        for i in range(index - 1, end - 1, -1):
            if highest < self.indicator.get_value(i):
                highest = self.indicator.get_value(i)
                
        return highest
