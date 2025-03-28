from decimal import Decimal

from pyta4j.indicators.cached_indicator import CachedIndicator

class AbstractEMAIndicator(CachedIndicator):
    def __init__(self, indicator, bar_count, multiplier: Decimal):
        super().__init__()  # Initialize CachedIndicator
        self.bar_count = bar_count
        self.multiplier = multiplier
        self.indicator = indicator

    def calculate(self, index: int) -> Decimal:
        if index == 0:
            return self.indicator.get_value(0)  # Base case
        else:
            prev_ema = self.get_value(index - 1)  # Use cached value
            price = self.indicator.get_value(index)
            return (price - prev_ema) * self.multiplier + prev_ema
