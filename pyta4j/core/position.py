from pyta4j.core.trade import Trade, TradeType
from pyta4j.cost.zero_cost_model import ZeroCostModel

class Position:
    def __init__(self, starting_type=TradeType.BUY, transaction_cost_model=None, holding_cost_model=None):
        self.starting_type = starting_type
        self.transaction_cost_model = transaction_cost_model if transaction_cost_model else ZeroCostModel()
        self.holding_cost_model = holding_cost_model if holding_cost_model else ZeroCostModel()
        self.entry = None
        self.exit = None

    def operate(self, index, price, amount):
        if self.is_new():
            trade = Trade(index, self.starting_type, price, amount, self.transaction_cost_model)
            self.entry = trade
            return trade
        elif self.is_opened():
            trade = Trade(index, self.starting_type.complement_type(), price, amount, self.transaction_cost_model)
            self.exit = trade
            return trade
        else:
            raise ValueError("Cannot operate on a closed position")

    def is_new(self):
        return self.entry is None and self.exit is None

    def is_opened(self):
        return self.entry is not None and self.exit is None

    def is_closed(self):
        return self.entry is not None and self.exit is not None

    def get_profit(self, final_index=None, final_price=None):
        if self.is_closed():
            gross_profit = self.exit.get_value() - self.entry.get_value()
            if self.entry.trade_type == TradeType.SELL:
                gross_profit = -gross_profit
            # Costs could be subtracted here; using zero costs for simplicity
            return gross_profit
        elif self.is_opened() and final_price is not None:
            hypothetical_exit_value = final_price * self.entry.amount
            gross_profit = hypothetical_exit_value - self.entry.get_value()
            if self.entry.trade_type == TradeType.SELL:
                gross_profit = -gross_profit
            return gross_profit
        return 0
    
    def has_profit(self):
        return self.get_profit() > 0
    
    def has_loss(self):
        return self.get_profit() < 0

    def get_gross_return(self):

        entry_price = self.entry.price_per_asset
        exit_price = self.exit.price_per_asset

        if entry_price == 0:
            raise ValueError("Entry price cannot be zero")
        
        ratio = exit_price / entry_price
        if self.entry.trade_type == TradeType.BUY:
            return ratio
        else:
            return 2 - ratio

    def get_holding_cost(self, final_index):
        return self.holding_cost_model.calculate(self, final_index)

    def __str__(self):
        return f"Position(entry={self.entry}, exit={self.exit})"