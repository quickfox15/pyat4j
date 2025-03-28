import unittest
from datetime import datetime, timedelta

from pyta4j.core.bar import Bar

class TestBar(unittest.TestCase):

    def setUp(self):
        self.begin_time = datetime(2014, 6, 25, 0, 0, 0)
        self.end_time =   datetime(2014, 6, 25, 1, 0, 0)
        self.duration = timedelta(hours=1)
        self.bar = Bar(self.duration, self.end_time)


    def test_bar_trade_add_trade(self):
        self.bar.add_trade(1.0, 100.0)
        assert self.bar.open_price == 100.0
        assert self.bar.high_price == 100.0
        assert self.bar.low_price == 100.0
        assert self.bar.close_price == 100.0
        assert self.bar.volume == 1.0
        assert self.bar.trades == 1
    
    def test_bar_trade_add_trade_multiple(self):
        self.bar.add_trade(1.0, 100.0)
        self.bar.add_trade(2.0, 200.0)
        assert self.bar.open_price == 100.0
        assert self.bar.high_price == 200.0
        assert self.bar.low_price == 100.0
        assert self.bar.close_price == 200.0
        assert self.bar.volume == 3.0
        assert self.bar.trades == 2
 
    def test_get_time_period(self):
        assert self.begin_time == self.bar.end_time - self.bar.duration

    def test_get_begin_time(self):
        assert self.begin_time == self.bar.begin_time

    def test_equals(self):
        bar1 = Bar(self.duration, self.end_time)
        bar2 = Bar(self.duration, self.end_time)

        self.assertEqual(bar1, bar2)

    def test_hash_code_equal(self):
        bar1 = Bar(self.duration, self.begin_time)
        bar2 = Bar(self.duration, self.begin_time)

        self.assertEqual(hash(bar1), hash(bar2))