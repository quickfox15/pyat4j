from pyta4j.indicators.cached_indicator import CachedIndicator
from pyta4j.indicators.ema_indicator import EMAIndicator

class MACDIndicator(CachedIndicator):
    def __init__(self, indicator, short_bar_count=12, long_bar_count=26):
        super().__init__()
        if short_bar_count > long_bar_count:
            raise ValueError("Long term period count must be greater than short term period count")
        self.short_term_ema = EMAIndicator(indicator, short_bar_count)
        self.long_term_ema = EMAIndicator(indicator, long_bar_count)


    def calculate(self, index):
        return self.short_term_ema.get_value(index) - self.long_term_ema.get_value(index)
