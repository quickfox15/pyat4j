from pyta4j.indicators import CachedIndicator

class TypicalPriceIndicator(CachedIndicator):
    
    def __init__(self, series):
        super().__init__()
        self.series = series
    
    def calculate(self, index):
        bar = self.series.get_bar(index)
        high_price = bar.high_price
        low_price = bar.low_price
        close_price = bar.close_price
        return high_price + low_price + close_price / 3
