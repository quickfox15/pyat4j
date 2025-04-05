from pyta4j.core.bar_series import BarSeries
from pyta4j.core.position import Position
from pyta4j.core.trade import TradeType
from pyta4j.core.trading_record import TradingRecord
from pyta4j.indicators.indicator import Indicator

class CashFlow(Indicator):
    """
    An indicator that tracks the cash flow of a trading strategy over a bar series.
    It calculates cash flow values based on positions or a trading record, accounting
    for both closed and open positions up to a specified final index.
    """
    
    def __init__(self, bar_series: BarSeries, arg):
        # Initialize the CashFlow indicator with a bar series and either a position or trading record.
        self.bar_series = bar_series
        self.values = [1]  # Initial cash flow value is 1
        
        # Handle different constructor signatures
        if isinstance(arg, Position):
            ## validate position is closed
            if not arg.is_closed():
                raise ValueError("Position is not closed. Final index of observation needs to be provided.")
            self.calculate_position(arg)

        elif isinstance(arg, TradingRecord):
            self.calculate_trading_record(arg)
        else:
            raise ValueError("Invalid argument type for CashFlow indicator.")

        self.fill_to_the_end()

    def get_value(self, index: int):
        return self.values[index]

    def get_bar_series(self) -> BarSeries:
        return self.bar_series

    def num_of(self, number: float):
        return number
    
    def get_size(self) -> int:
        return self.bar_series.get_bar_count()

    def calculate_position(self, position: Position):

        final_index = position.exit.index
        is_long_trade = position.entry.trade_type == TradeType.BUY
        end_index = self.determine_end_index(position, final_index, self.bar_series.series_end_index)
        entry_index = position.entry.index
        begin = entry_index + 1
        
        # Extend values list if necessary
        if begin > len(self.values):
            last_value = self.values[-1]
            self.values.extend([last_value] * (begin - len(self.values)))
        
        # Proceed only if the last value is positive
        if self.values[-1] > self.num_of(0):
            starting_index = max(begin, 1)

            n_periods = end_index - entry_index
            holding_cost = position.get_holding_cost(end_index)
            avg_cost = holding_cost / self.num_of(n_periods) if n_periods > 0 else 0
            net_entry_price = position.entry.net_price
            
            # Add intermediate cash flows
            for i in range(starting_index, end_index):
                intermediate_net_price = self.add_cost(
                    self.bar_series.get_bar(i).close_price, avg_cost, is_long_trade
                )
                ratio = self.get_intermediate_ratio(is_long_trade, net_entry_price, intermediate_net_price)
                self.values.append(self.values[entry_index] * ratio)
            
            # Add cash flow at exit
            if position.exit is not None:
                exit_price = position.exit.net_price
            else:
                exit_price = self.bar_series.get_bar(end_index).close_price
            exit_net_price = self.add_cost(exit_price, avg_cost, is_long_trade)
            ratio = self.get_intermediate_ratio(is_long_trade, net_entry_price, exit_net_price)
            self.values.append(self.values[entry_index] * ratio)

    def calculate_trading_record(self, trading_record: TradingRecord):
        for position in trading_record.get_positions():
            self.calculate_position(position)

    def calculate(self, arg):
        if isinstance(arg, Position):
            self.calculate_position(arg)
        elif isinstance(arg, TradingRecord):
            self.calculate_trading_record(arg)
        else:
            raise ValueError("Invalid argument type for CashFlow indicator.")

    @staticmethod
    def add_cost(raw_price, holding_cost, is_long_trade: bool):
        if is_long_trade:
            net_price = raw_price - holding_cost
        else:
            net_price = raw_price + holding_cost
        return net_price

    @staticmethod
    def get_intermediate_ratio(is_long_trade: bool, entry_price, exit_price) :
        if is_long_trade:
            ratio = exit_price / entry_price
        else:
            ratio = 2 - (exit_price / entry_price)
        return ratio

    @staticmethod
    def determine_end_index(position: Position, final_index: int, max_index: int) -> int:
        idx = position.exit.index if position.exit is not None else final_index
        return min(idx, final_index, max_index)

    def fill_to_the_end(self):
        if self.bar_series.series_end_index >= len(self.values):
            last_value = self.values[-1]
            self.values.extend([last_value] * (self.bar_series.series_end_index - len(self.values) + 1))