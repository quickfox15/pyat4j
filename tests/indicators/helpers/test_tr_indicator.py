from datetime import datetime, timedelta, timezone
import unittest


from pyta4j.indicators.helpers.tr_indicator import TRIndicator
from tests.utils.mocks import MockBar, MockBarSeries


class TestTRIndicator(unittest.TestCase):

    def test_tr_indicator(self):

        bars = []
        bars.append(MockBar(0, 12, 15, 8))
        bars.append(MockBar(0, 8, 11, 6))
        bars.append(MockBar(0, 15, 17, 14))
        bars.append(MockBar(0, 15, 17, 14))
        bars.append(MockBar(0, 0, 0, 2))
        tr = TRIndicator(MockBarSeries(bars))
        
        self.assertAlmostEqual(7, tr.get_value(0))
        self.assertAlmostEqual(6, tr.get_value(1))
        self.assertAlmostEqual(9, tr.get_value(2))
        self.assertAlmostEqual(3, tr.get_value(3))
        self.assertAlmostEqual(15, tr.get_value(4))
        


        # List<Bar> bars = new ArrayList<Bar>();
        # bars.add(new MockBar(0, 12, 15, 8, numFunction));
        # bars.add(new MockBar(0, 8, 11, 6, numFunction));
        # bars.add(new MockBar(0, 15, 17, 14, numFunction));
        # bars.add(new MockBar(0, 15, 17, 14, numFunction));
        # bars.add(new MockBar(0, 0, 0, 2, numFunction));
        # TRIndicator tr = new TRIndicator(new MockBarSeries(bars));

        # assertNumEquals(7, tr.getValue(0));
        # assertNumEquals(6, tr.getValue(1));
        # assertNumEquals(9, tr.getValue(2));
        # assertNumEquals(3, tr.getValue(3));
        # assertNumEquals(15, tr.getValue(4));