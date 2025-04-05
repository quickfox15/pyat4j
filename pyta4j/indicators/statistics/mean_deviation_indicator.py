from pyta4j.indicators.cached_indicator import CachedIndicator
from pyta4j.indicators.sma_indicator import SMAIndicator

class MeanDeviationIndicator(CachedIndicator):
    def __init__(self, indicator, bar_count):
        super().__init__()
        self.indicator = indicator
        self.bar_count = bar_count
        self.sma = SMAIndicator(indicator, bar_count)

    def calculate(self, index):
        absolute_deviations = 0
        average = self.sma.get_value(index)
        start_index = max(0, index - self.bar_count + 1)
        nb_values = index - start_index + 1
        for i in range(start_index, index + 1):
            absolute_deviations += abs(self.indicator.get_value(i) - average)
        return absolute_deviations / nb_values
