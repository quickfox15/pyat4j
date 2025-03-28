from decimal import Decimal
from pyta4j.core.trade import TradeType
from pyta4j.rules.rule import Rule

class StopGainRule(Rule):
    def __init__(self, indicator, gain_percentage):
        self.indicator = indicator
        self.gain_percentage = Decimal(str(gain_percentage))

    def is_satisfied(self, index, trading_record):

        if trading_record is None or trading_record.is_closed():
            return False
        
        position = trading_record.get_current_position()
        if position.is_new():
            return False
        
        entry_price = position.entry.net_price
        current_price = Decimal(str(self.indicator.get_value(index)))

        if position.entry.trade_type == TradeType.BUY:
            return self.is_buy_gain_satisfied(entry_price, current_price)
        else:
            return self.is_sell_gain_satisfied(entry_price, current_price)

    def is_buy_gain_satisfied(self, entry_price, current_price):
        loss_ratio_threshold = Decimal('1') + self.gain_percentage / Decimal('100')
        threshold = entry_price * loss_ratio_threshold
        return current_price >= threshold

    def is_sell_gain_satisfied(self, entry_price, current_price):
        loss_ratio_threshold = Decimal('1') - self.gain_percentage / Decimal('100')
        threshold = entry_price * loss_ratio_threshold
        return current_price <= threshold

