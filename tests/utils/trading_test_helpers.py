from datetime import datetime, timedelta, timezone
from decimal import Decimal

from pyta4j.core.bar import Bar,BarSeries
from pyta4j.core.trading_record import TradingRecord

def populate_bar_series(prices)->BarSeries:
    duration = timedelta(hours=1)
    end_time = datetime(2014, 6, 25, 1, 0, 0, tzinfo=timezone.utc)
    bar_series = BarSeries('test')
    for price in prices:
        bar = Bar(duration, end_time)
        bar.add_trade(1, price)
        bar_series.add_bar(bar)
        end_time += duration
    return bar_series

def populate_trading_record(trade_type, indices, bar_series)->TradingRecord:
    trading_record = TradingRecord(trade_type)

    for i in indices:
        price = bar_series.bars[i].close_price
        volume = bar_series.bars[i].volume
        if trading_record.is_closed():
            trading_record.enter(i, price, volume)
        else:
            trading_record.exit(i, price, volume)

    return trading_record

def dec(value):
    return Decimal(str(value))
