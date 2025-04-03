from pyta4j.indicators import CachedIndicator

class BollingerBandsMiddleIndicator(CachedIndicator):
    
    def __init__(self, indicator):
        super().__init__()
        self.indicator = indicator
        
    def calculate(self, index):
        return self.indicator.get_value(index)

