from decimal import Decimal
from pyta4j.indicators.cached_indicator import CachedIndicator
from pyta4j.indicators.helpers.typical_price_indicator import TypicalPriceIndicator
from pyta4j.indicators.sma_indicator import SMAIndicator
from pyta4j.indicators.statistics.mean_deviation_indicator import MeanDeviationIndicator

class CCIIndicator(CachedIndicator):
    
    def __init__(self, series, bar_count, factor=0.015):
        super().__init__()
        self.factor = Decimal(factor)
        self.typical_price_ind = TypicalPriceIndicator(series)
        self.sma_ind = SMAIndicator(self.typical_price_ind, bar_count)
        self.mean_deviation_ind = MeanDeviationIndicator(self.typical_price_ind, bar_count)
        self.bar_count = bar_count
    
    def calculate(self, index):
        typical_price = self.typical_price_ind.get_value(index)
        typical_price_avg = self.sma_ind.get_value(index)
        mean_deviation = self.mean_deviation_ind.get_value(index)
        if mean_deviation == 0:
            return Decimal(0)
        return (typical_price - typical_price_avg) / (mean_deviation * self.factor)
