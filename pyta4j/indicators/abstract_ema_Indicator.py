from pyta4j.indicators.recursive_cached_indicator import RecursiveCachedIndicator

class AbstractEMAIndicator(RecursiveCachedIndicator):
    def __init__(self, indicator, bar_count, multiplier):
        super().__init__()  # Initialize CachedIndicator
        self.bar_count = bar_count
        self.multiplier = multiplier
        self.indicator = indicator

    def calculate(self, index: int):
        if index == 0:
            return self.indicator.get_value(0)  # Base case
        else:
            prev_ema = self.get_value(index - 1)  # Use cached value
            price = self.indicator.get_value(index)
            return (price - prev_ema) * self.multiplier + prev_ema
