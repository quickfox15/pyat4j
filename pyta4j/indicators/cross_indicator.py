
from pyta4j.indicators.cached_indicator import CachedIndicator

class CrossIndicator(CachedIndicator):

    def __init__(self, up, low):
        super().__init__()
        self.up = up  # Upper indicator (e.g., short SMA)
        self.low = low  # Lower indicator (e.g., long SMA or constant)

    def calculate(self, index):
        if index == 0 or self.up.get_value(index) >= self.low.get_value(index):
            return False
        
        i = index - 1
        if self.up.get_value(i) > self.low.get_value(i):
            return True
        
        while i > 0 and self.up.get_value(i) == self.low.get_value(i):
            i -= 1
        return i != 0 and self.up.get_value(i) > self.low.get_value(i)
