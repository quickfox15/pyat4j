
from decimal import Decimal

from pyta4j.indicators.cached_indicator import CachedIndicator
from pyta4j.indicators.helpers.gain_indicator import GainIndicator
from pyta4j.indicators.helpers.loss_indicator import LossIndicator
from pyta4j.indicators.mma_indicator import MMAIndicator

class RSIIndicator(CachedIndicator):

    def __init__(self, indicator, bar_count):
        super().__init__()
        self.indicator = indicator
        self.average_gain_indicator = MMAIndicator(GainIndicator(indicator), bar_count)
        self.average_loss_indicator = MMAIndicator(LossIndicator(indicator), bar_count)


    def get_value(self, index):
        return self.calculate(index)

    def calculate(self, index)->Decimal:
        average_gain = self.average_gain_indicator.get_value(index)
        average_loss = self.average_loss_indicator.get_value(index)
        if average_loss == 0:
            if average_gain == 0:
                return 0
            else:
                return 100
        relative_strength = average_gain / average_loss
        return 100 - 100 / (1 + relative_strength)
