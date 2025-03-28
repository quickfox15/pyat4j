from decimal import Decimal
from enum import Enum
from pyta4j.cost.zero_cost_model import ZeroCostModel

class TradeType(Enum):
    BUY = "BUY"
    SELL = "SELL"

    def complement_type(self):
        return TradeType.SELL if self == TradeType.BUY else TradeType.BUY

class Trade:
    def __init__(self, index, trade_type, price_per_asset, amount, cost_model=None):
        self.index = index
        self.trade_type = trade_type
        self.amount = Decimal(str(amount))
        self.price_per_asset = Decimal(str(price_per_asset))

        self.cost_model = cost_model if cost_model else ZeroCostModel()
        self.cost = self.cost_model.calculate_price_amount(self.price_per_asset, self.amount)

        cost_per_asset = self.cost / self.amount
        self.net_price = (self.price_per_asset + cost_per_asset if trade_type == TradeType.BUY 
                          else self.price_per_asset - cost_per_asset)

    def get_value(self):
        return self.price_per_asset * self.amount

    @staticmethod
    def buy_at( index, price, amount, cost_model=None):
        return Trade(index, TradeType.BUY, price, amount, cost_model)

    @staticmethod
    def sell_at(index, price, amount, cost_model=None):
        return Trade(index, TradeType.SELL, price, amount, cost_model)

    def __str__(self):
        return f"Trade(type={self.trade_type}, index={self.index}, price={self.price_per_asset}, amount={self.amount})"