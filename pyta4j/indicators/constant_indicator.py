from pyta4j.indicators.indicator import Indicator

class ConstantIndicator(Indicator):
    def __init__(self, value):
        self.value = value

    def get_value(self, index):
        return self.value