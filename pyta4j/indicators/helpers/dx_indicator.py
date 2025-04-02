from pyta4j.indicators import CachedIndicator
from pyta4j.indicators.adx.plus_di_indicator import PlusDIIndicator
from pyta4j.indicators.adx.minus_di_indicator import MinusDIIndicator

class DXIndicator(CachedIndicator):
    
    def __init__(self, series,barCount):
        super().__init__()
        self.series = series
        self.barCount = barCount
        self.plus_di_indicator = PlusDIIndicator(series, barCount)
        self.minus_di_indicator = MinusDIIndicator(series, barCount)

    def calculate(self, index):
        pdi_value = self.plus_di_indicator.get_value(index)
        mdi_value = self.minus_di_indicator.get_value(index)
        if pdi_value + mdi_value == 0:
            return 0
        return abs(pdi_value - mdi_value) / (pdi_value + mdi_value) * 100
