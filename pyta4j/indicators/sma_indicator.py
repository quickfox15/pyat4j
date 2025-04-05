import numpy as np
from pyta4j.indicators.cached_indicator import CachedIndicator

class SMAIndicator(CachedIndicator):
    def __init__(self, indicator, bar_count):
        super().__init__()
        self.indicator = indicator
        self.bar_count = bar_count

    def calculate(self, index):
        total = 0
        start = max(0, index - self.bar_count + 1)
        for i in range(start, index + 1):
            total += self.indicator.get_value(i)
        real_bar_count = min(self.bar_count, index + 1)
        return total / real_bar_count
    
    #test with numpy and pandas

    def get_value_numpy(self, index):
        start = max(0, index - self.bar_count + 1)
        values = [self.indicator.get_value(i) for i in range(start, index + 1)]
        return float(np.mean(values))  # Matches TA4J's real_bar_count logic

