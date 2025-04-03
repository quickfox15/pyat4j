from pyta4j.indicators import CachedIndicator

class BollingerBandsLowerIndicator(CachedIndicator):

    def __init__(self, bbm, indicator=None, k=2.0):
        super().__init__()
        self.bbm = bbm
        # if indicator is None: get bbm's indicator
        if indicator is None:
            self.indicator = bbm.indicator
        else:
            self.indicator = indicator
        self.indicator = indicator
        self.k = k
    
    def calculate(self, index):
        return self.bbm.get_value(index) - (self.indicator.get_value(index) * self.k)
    