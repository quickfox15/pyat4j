from datetime import datetime, timedelta, timezone

from pyta4j.core.bar_series import BarSeries
from pyta4j.core.bar import Bar

class MockBar(Bar):
    
    def __init__(self, open_price, close_price, high_price, low_price):
        super().__init__(timedelta(hours=1), datetime(2014, 6, 25, 1, 0, 0, tzinfo=timezone.utc))
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        
        
class MockBarSeries(BarSeries):
    
    def __init__(self, bars):
        super().__init__("test")
        for bar in bars:
            self.add_bar(bar)
            
    def add_bar(self, bar):
        self.bars.append(bar)
        
    def get_bar(self, index):
        return self.bars[index]
        
    def get_bar_count(self):
        return len(self.bars)