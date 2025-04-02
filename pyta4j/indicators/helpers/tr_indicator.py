from pyta4j.indicators import CachedIndicator

class TRIndicator(CachedIndicator):
    
    def __init__(self, series):
        super().__init__()
        self.series = series
        
    def calculate(self, index):
        ts = self.series.get_bar(index).high_price - self.series.get_bar(index).low_price
        ys = 0 if index == 0 else self.series.get_bar(index).high_price - self.series.get_bar(index - 1).close_price
        yst = 0 if index == 0 else self.series.get_bar(index - 1).close_price - self.series.get_bar(index).low_price
        return max(abs(ts), abs(ys), abs(yst))
