from pyta4j.indicators import CachedIndicator, MMAIndicator, TRIndicator

class ATRIndicator(CachedIndicator):
    
    def __init__(self, series, bar_count):
        super().__init__()
        self.average_true_range_indicator = MMAIndicator(TRIndicator(series), bar_count)
    
    def calculate(self, index):
        return self.average_true_range_indicator.get_value(index)
