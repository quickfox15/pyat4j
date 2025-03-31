from pyta4j.core.trade import TradeType
from pyta4j.core.position import Position
from pyta4j.cost.zero_cost_model import ZeroCostModel

class TradingRecord:
    def __init__(self, starting_type=TradeType.BUY, transaction_cost_model=None, holding_cost_model=None, name=None):
        self.name = name
        self.starting_type = starting_type
        self.transaction_cost_model = transaction_cost_model if transaction_cost_model else ZeroCostModel()
        self.holding_cost_model = holding_cost_model if holding_cost_model else ZeroCostModel()
        self.trades = []
        self.buy_trades = []
        self.sell_trades = []
        self.entry_trades = []
        self.exit_trades = []
        self.positions = []
        self.current_position = Position(starting_type, self.transaction_cost_model, self.holding_cost_model)

    def initialize_from_trades(self, trades):
        for trade in trades:
            is_entry = self.current_position.is_new()
            if is_entry and trade.trade_type != self.starting_type:
                #  Special case for entry/exit types reversal
                #  E.g.: BUY, SELL,
                #  BUY, SELL,
                #  SELL, BUY,
                # r BUY, SELL
                self.current_position = Position(trade.trade_type, self.transaction_cost_model, self.holding_cost_model)
            new_trade = self.operate(trade.index, trade.price_per_asset, trade.amount)
            self.record_trade(new_trade, is_entry)

    def operate(self, index, price, amount):

        if self.current_position.is_closed():
            raise ValueError("Current position is closed")
        
        is_entry = self.current_position.is_new()
        trade = self.current_position.operate(index, price, amount)

        self.record_trade(trade, is_entry)
        if self.current_position.is_closed():
            self.positions.append(self.current_position)
            self.current_position = Position(self.starting_type, self.transaction_cost_model, self.holding_cost_model)
        return trade

    def enter(self, index, price, amount):
        if self.current_position.is_new():
            return self.operate(index, price, amount)
        return None

    def exit(self, index, price, amount):
        if self.current_position.is_opened():
            return self.operate(index, price, amount)
        return None

    def record_trade(self, trade, is_entry):
        self.trades.append(trade)
        if trade.trade_type == TradeType.BUY:
            self.buy_trades.append(trade)
        else:
            self.sell_trades.append(trade)
        if is_entry:
            self.entry_trades.append(trade)
        else:
            self.exit_trades.append(trade)

    def is_closed(self):
        return not self.current_position.is_opened()

    def get_current_position(self):
        return self.current_position

    def get_positions(self):
        return self.positions

    def get_last_trade(self):
        return self.trades[-1] if self.trades else None

    def __str__(self):
        return f"TradingRecord(name={self.name}, trades={self.trades})"