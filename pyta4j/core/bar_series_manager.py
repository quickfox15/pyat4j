from decimal import Decimal
from pyta4j.cost.zero_cost_model import ZeroCostModel

from pyta4j.core.bar_series import BarSeries
from pyta4j.core.strategy import Strategy
from pyta4j.core.trade import TradeType
from pyta4j.core.trading_record import TradingRecord

class BarSeriesManager:
    def __init__(self, series:BarSeries, transaction_cost_model=None, holding_cost_model=None):
        self.series = series
        self.transaction_cost_model = transaction_cost_model if transaction_cost_model else ZeroCostModel()
        self.holding_cost_model = holding_cost_model if holding_cost_model else ZeroCostModel()

    def run(self, strategy:Strategy, trade_type=None, amount=None, start_index=None, finish_index=None):
        if trade_type is None:
            trade_type = TradeType.BUY
        if amount is None:
            amount = Decimal(1)
        if start_index is None:
            start_index = self.series.series_begin_index
        if finish_index is None:
            finish_index = self.series.series_end_index

        run_begin_index = max(start_index, self.series.series_begin_index)
        run_end_index = min(finish_index, self.series.series_end_index)
        
        """Run the strategy over the bar series and return a TradingRecord."""
        trading_record = TradingRecord(trade_type, self.transaction_cost_model, self.holding_cost_model)

        for index in range(run_begin_index, run_end_index+1):
            if(strategy.should_operate(index, trading_record)):
                trading_record.operate(index, self.series.get_bar(index).close_price, amount)

        if not trading_record.is_closed():
        #     If the last position is still opened, we search out of the run end index.
        #     May works if the end index for this run was inferior to the actual number of
        #     bars
            series_max_size = max(self.series.series_end_index + 1, len(self.series.bars))
            for i in range(run_end_index + 1, series_max_size):
        #         For each bar after the end index of this run...
        #          --> Trying to close the last position
                if strategy.should_operate(i, trading_record):
                    trading_record.operate(i, self.series.get_bar(i).close_price, amount)
                    break

        return trading_record
