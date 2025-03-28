import csv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pyta4j.core.bar import Bar
from pyta4j.core.bar_series import BarSeries

class CsvTradesLoader:
    @staticmethod
    def load_bitstamp_series():
        series = BarSeries("Bitstamp Series")
        
        try:
            with open("tests/resources/bitstamp_trades_from_20131125_usd.csv", "r", encoding="utf-8") as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip header
                lines = list(csv_reader)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return series

        if not lines:
            return series

        # Ensure oldest-to-newest order
        first_ts = int(lines[0][0])
        last_ts = int(lines[-1][0])
        if first_ts > last_ts:
            lines = lines[::-1]
            begin_ts, end_ts = last_ts, first_ts
        else:
            begin_ts, end_ts = first_ts, last_ts

        begin_time = datetime.fromtimestamp(begin_ts, tz=ZoneInfo("UTC"))
        end_time = datetime.fromtimestamp(end_ts, tz=ZoneInfo("UTC"))
        CsvTradesLoader._build_series(series, begin_time, end_time, 300, lines)
        return series

    @staticmethod
    def _build_series(series, begin_time, end_time, duration, lines):
        bar_duration = timedelta(seconds=duration)
        bar_end_time = begin_time
        i = 0

        while bar_end_time < end_time and i < len(lines):
            bar_end_time += bar_duration
            bar = Bar(bar_duration, bar_end_time)
            
            while i < len(lines):
                trade_time = datetime.fromtimestamp(int(lines[i][0]), tz=ZoneInfo("UTC"))
                if bar.in_period(trade_time):
                    bar.add_trade(float(lines[i][2]), float(lines[i][1]))  # Volume, Price
                    i += 1
                else:
                    break
            
            if bar.trades > 0:  # Direct attribute access
                series.add_bar(bar)

    @staticmethod
    def main():
        series = CsvTradesLoader.load_bitstamp_series()
        print(f"Series: {series.get_name()} ({series.get_series_period_description()})")
        print(f"Number of bars: {series.get_bar_count()}")
        if series.get_bar_count() > 0:
            first_bar = series.get_bar(0)
            print("First bar:")
            print(f"\tVolume: {first_bar.volume}")
            print(f"\tNumber of trades: {first_bar.trades}")
            print(f"\tClose price: {first_bar.close_price}")
            #print index and close price of each bar
            for i in range(series.get_bar_count()-1000):
                print(f"Bar {i}: {series.get_bar(i).close_price}")

if __name__ == "__main__":
    CsvTradesLoader.main()