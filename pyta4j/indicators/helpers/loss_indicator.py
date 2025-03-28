from pyta4j.indicators.cached_indicator import CachedIndicator

class LossIndicator(CachedIndicator):
    def __init__(self, indicator):
        super().__init__()
        self.indicator = indicator

    def calculate(self, index):
        if index == 0:
            return 0
        if self.indicator.get_value(index) < self.indicator.get_value(index - 1):
            return self.indicator.get_value(index - 1) - self.indicator.get_value(index)
        else:
            return 0