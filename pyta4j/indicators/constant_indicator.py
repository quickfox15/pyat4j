from decimal import Decimal

from pyta4j.indicators.indicator import Indicator

class ConstantIndicator(Indicator):
    def __init__(self, value):
        self.value = self._to_decimal(value)

    def _to_decimal(self, value):
        if isinstance(value, Decimal):
            return value
        return Decimal(str(value))  # Handles float and int safely

    def get_value(self, index):
        return self.value