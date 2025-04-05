from pyta4j.indicators import CachedIndicator

class MinusDMIndicator(CachedIndicator):
    
    def __init__(self, series):
        super().__init__()
        self.series = series
        
    def calculate(self, index):
        if index == 0:
            return 0
        prevBar = self.series.get_bar(index - 1)
        currentBar = self.series.get_bar(index)
        upMove = currentBar.high_price - prevBar.high_price
        downMove = prevBar.low_price - currentBar.low_price
        if downMove > upMove and downMove > 0:
            return downMove
        else:
            return 0
    
