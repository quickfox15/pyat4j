from pyta4j.indicators import CachedIndicator

class PlusDMIndicator(CachedIndicator):
    
    def __init__(self, series):
        super().__init__()
        self.series = series
    
    def calculate(self, index):
        if index == 0:
            return 0
        prev_bar = self.series.get_bar(index - 1)
        current_bar = self.series.get_bar(index)
        up_move = current_bar.high_price - prev_bar.high_price
        down_move = prev_bar.low_price - current_bar.low_price
        if up_move > down_move and up_move > 0:
            return up_move
        else:
            return 0
