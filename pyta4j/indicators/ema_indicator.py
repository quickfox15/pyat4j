
from pyta4j.indicators.abstract_ema_Indicator import AbstractEMAIndicator

class EMAIndicator(AbstractEMAIndicator):
    def __init__(self, indicator, bar_count):
        multiplier = 2 / (bar_count + 1)
        super().__init__(indicator, bar_count, multiplier)

