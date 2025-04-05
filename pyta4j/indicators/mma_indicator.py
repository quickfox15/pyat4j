from pyta4j.indicators.abstract_ema_Indicator import AbstractEMAIndicator

class MMAIndicator(AbstractEMAIndicator):
    def __init__(self, indicator, bar_count):
        multiplier = 1 / bar_count
        super().__init__(indicator, bar_count, multiplier)
