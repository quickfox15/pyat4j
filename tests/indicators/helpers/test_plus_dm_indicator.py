from datetime import datetime, timedelta, timezone
import unittest


from pyta4j.indicators import PlusDMIndicator
from tests.utils.mocks import MockBar, MockBarSeries


class TestPlusDMIndicator(unittest.TestCase):

    def test_zero_directional_movement(self):
        yesterdayBar = MockBar(0, 0, 10, 2)
        todayBar = MockBar(0, 0, 6, 6)
        bars = []
        bars.append(yesterdayBar)
        bars.append(todayBar)
        series = MockBarSeries(bars)
        dup = PlusDMIndicator(series)
        self.assertAlmostEqual(0, dup.get_value(1))

    def test_zero_directional_movement2(self):
        yesterdayBar = MockBar(0, 0, 6, 12)
        todayBar = MockBar(0, 0, 12, 6)
        bars = []
        bars.append(yesterdayBar)
        bars.append(todayBar)
        series = MockBarSeries(bars)
        dup = PlusDMIndicator(series)
        self.assertAlmostEqual(0, dup.get_value(1))

    def test_zero_directional_movement3(self):
        yesterdayBar = MockBar(0, 0, 6, 20)
        todayBar = MockBar(0, 0, 12, 4)
        bars = []
        bars.append(yesterdayBar)
        bars.append(todayBar)
        series = MockBarSeries(bars)
        dup = PlusDMIndicator(series)
        self.assertAlmostEqual(0, dup.get_value(1))
        
    def test_positive_directional_movement(self):
        yesterdayBar = MockBar(0, 0, 6, 6)
        todayBar = MockBar(0, 0, 12, 4)
        bars = []
        bars.append(yesterdayBar)
        bars.append(todayBar)
        series = MockBarSeries(bars)
        dup = PlusDMIndicator(series)
        self.assertAlmostEqual(6, dup.get_value(1))
        