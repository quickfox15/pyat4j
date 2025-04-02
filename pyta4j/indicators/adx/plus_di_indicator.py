from pyta4j.indicators import CachedIndicator,PlusDMIndicator
from pyta4j.indicators.mma_indicator import MMAIndicator
from pyta4j.indicators.atr_indicator import ATRIndicator

class PlusDIIndicator(CachedIndicator):
    
    def __init__(self, series, bar_count):
        super().__init__()
        self.avg_plus_dm_indicator = MMAIndicator(PlusDMIndicator(series), bar_count)
        self.atr_indicator = ATRIndicator(series, bar_count)
        self.bar_count = bar_count

    def calculate(self, index):
        return self.avg_plus_dm_indicator.get_value(index) / self.atr_indicator.get_value(index) * 100
