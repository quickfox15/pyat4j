from pyta4j.indicators.cached_indicator import CachedIndicator

class LowPriceIndicator(CachedIndicator):
    def __init__(self, series):
        super().__init__()
        self.series = series

    def calculate(self, index):
        return self.series.get_bar(index).low_price