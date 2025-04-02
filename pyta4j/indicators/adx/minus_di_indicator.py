from pyta4j.indicators import CachedIndicator,MMAIndicator,MinusDMIndicator
from pyta4j.indicators.atr_indicator import ATRIndicator

class MinusDIIndicator(CachedIndicator):
    
    def __init__(self, series, bar_count):
        super().__init__()
        self.avg_minus_dm_indicator = MMAIndicator(MinusDMIndicator(series), bar_count)
        self.atr_indicator = ATRIndicator(series, bar_count)
        self.bar_count = bar_count

    def calculate(self, index):
        return self.avg_minus_dm_indicator.get_value(index) / self.atr_indicator.get_value(index) * 100
