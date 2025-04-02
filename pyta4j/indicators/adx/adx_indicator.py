from pyta4j.indicators import CachedIndicator,MMAIndicator,DXIndicator

class ADXIndicator(CachedIndicator):
    
    def __init__(self, series, di_bar_count, adx_bar_count=None):
        super().__init__()
        self.series = series
        self.di_bar_count = di_bar_count
        self.adx_bar_count = adx_bar_count if adx_bar_count is not None else di_bar_count
        self.average_dx_indicator = MMAIndicator(DXIndicator(series, di_bar_count), adx_bar_count)


    def calculate(self, index):
        return self.average_dx_indicator.get_value(index)
