from pyta4j.core.trading_record import TradingRecord

class BarSeriesManager:
    def __init__(self, series):
        self.series = series

    def run(self, strategy):
        """Run the strategy over the bar series and return a TradingRecord."""
        trading_record = TradingRecord()
        for index in range(len(self.series.bars)):
            current_bar = self.series.get_bar(index)
            if strategy.should_enter(index, trading_record):
                # Enter a position with price and amount (e.g., 1 unit)
                trading_record.enter(index, current_bar.close_price, 1)
            elif strategy.should_exit(index, trading_record):
                # Exit the position with price and amount
                trading_record.exit(index, current_bar.close_price, 1)
        return trading_record