import unittest
from datetime import datetime, timedelta

from pyta4j.core.bar import Bar
from pyta4j.core.bar_series import BarSeries


class TestBarSeries(unittest.TestCase):

    def setUp(self):
        self.duration = timedelta(hours=1)

        self.bars = [
            Bar(self.duration, datetime(2014, 6, 13)),
            Bar(self.duration, datetime(2014, 6, 14)),
            Bar(self.duration, datetime(2014, 6, 15)),
            Bar(self.duration, datetime(2014, 6, 20)),
            Bar(self.duration, datetime(2014, 6, 25)),
            Bar(self.duration, datetime(2014, 6, 30)),
        ]

        # Add trades to each bar so close price is set
        for i, bar in enumerate(self.bars):
            bar.add_trade(1, float(i + 1))  # Prices: 1.0, 2.0, ..., 6.0

        default_name = "Series Name"
        self.default_series = BarSeries(default_name, self.bars)

    def test_bar_series_loaded(self):
        self.assertEqual(len(self.default_series.bars), 6)
        self.assertEqual(self.default_series.bars[0].close_price, 1.0)
        self.assertEqual(self.default_series.bars[-1].end_time, datetime(2014, 6, 30))

    def test_bar_series_add_bar(self):
        new_bar = Bar(self.duration, datetime(2014, 7, 1))
        new_bar.add_trade(1, 7.0)
        self.default_series.add_bar(new_bar)
        self.assertEqual(len(self.default_series.bars), 7)
        self.assertEqual(self.default_series.bars[-1].close_price, 7.0)

    def test_bar_series_add_bar_replace(self):
        new_bar = Bar(self.duration, datetime(2014, 6, 30))
        new_bar.add_trade(1, 7.0)
        self.default_series.add_bar(new_bar, True)
        self.assertEqual(len(self.default_series.bars), 6)
        self.assertEqual(self.default_series.bars[-1].close_price, 7.0)

    def test_empty_series_indexes(self):
        series = BarSeries("EmptySeries")
        self.assertEqual(series.series_begin_index, -1)
        self.assertEqual(series.series_end_index, -1)

    def test_single_bar_series_indexes(self):
        bar = Bar(timedelta(hours=1), datetime(2025, 1, 1, 9, 0))
        bar.add_trade(1, 100)
        
        series = BarSeries("SingleBar")
        series.add_bar(bar)

        self.assertEqual(series.series_begin_index, 0)
        self.assertEqual(series.series_end_index, 0)

    def test_multiple_bars_series_indexes(self):
        series = BarSeries("MultiBar")
        start_time = datetime(2025, 1, 1, 9, 0)
        duration = timedelta(hours=1)

        for i in range(5):
            bar = Bar(duration, start_time + i * duration)
            bar.add_trade(1, 100 + i)
            series.add_bar(bar)

        self.assertEqual(series.series_begin_index, 0)
        self.assertEqual(series.series_end_index, 4)

    def test_preloaded_bars_initializes_indexes(self):
        bars = []
        duration = timedelta(hours=1)
        start_time = datetime(2025, 1, 1, 9, 0)

        for i in range(3):
            bar = Bar(duration, start_time + i * duration)
            bar.add_trade(1, 100 + i)
            bars.append(bar)

        series = BarSeries("Preloaded", bars)

        self.assertEqual(series.series_begin_index, 0)
        self.assertEqual(series.series_end_index, 2)

    def test_series_indexes_after_max_limit(self):
        series = BarSeries("Limited")
        series.maximum_bar_count = 3

        duration = timedelta(hours=1)
        time = datetime(2025, 1, 1, 0, 0)

        for i in range(5):
            bar = Bar(duration, time + i * duration)
            bar.add_trade(1, 100 + i)
            series.add_bar(bar)

        self.assertEqual(len(series.bars), 3)
        self.assertEqual(series.series_begin_index, 0)
        self.assertEqual(series.series_end_index, 4)
        self.assertEqual(series.removed_bars_count, 2)

    def test_get_bar_after_removal(self):
        series = BarSeries("CompatTest")
        series.set_maximum_bar_count(3)

        start_time = datetime(2025, 1, 1, 0, 0)
        duration = timedelta(hours=1)

        for i in range(5):  # 5 bars, only last 3 remain
            bar = Bar(duration, start_time + i * duration)
            bar.add_trade(1, 100 + i)
            series.add_bar(bar)

        # series_end_index = 4, series_begin_index = 0, removed_bars_count = 2
        self.assertEqual(series.series_end_index, 4)
        self.assertEqual(series.series_begin_index, 0)
        self.assertEqual(series.removed_bars_count, 2)

        self.assertEqual(series.get_bar(2).close_price, 102)
        self.assertEqual(series.get_bar(4).close_price, 104)
