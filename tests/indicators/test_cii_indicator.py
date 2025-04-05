
import unittest

from pyta4j.indicators.cci_indicator import CCIIndicator
from tests.utils.trading_test_helpers import populate_bar_series


class TestCCIIndicator(unittest.TestCase):
    
    def setUp(self):
        data = [23.98, 23.92, 23.79, 23.67, 23.54, 23.36, 23.65, 23.72, 24.16,
             23.91, 23.81, 23.92, 23.74, 24.68, 24.94, 24.93, 25.10, 25.12, 25.20, 25.06, 24.50, 24.31, 24.57, 24.62,
             24.49, 24.37, 24.41, 24.35, 23.75, 24.09]
        self.series = populate_bar_series(data)

    def test_get_value_when_bar_count_is20(self):
        cci = CCIIndicator(self.series, 20)

        # Incomplete time frame
        self.assertAlmostEqual((0), cci.get_value(0))
        self.assertAlmostEqual((-66.6667), cci.get_value(1), 4)
        self.assertAlmostEqual((-100), cci.get_value(2), 4)
        self.assertAlmostEqual((14.365), cci.get_value(10), 4)
        self.assertAlmostEqual((54.2544), cci.get_value(11), 4)

        # Complete time frame
        results20to30 = [101.9185, 31.1946, 6.5578, 33.6078, 34.9686, 13.6027, -10.6789, -11.471,
                -29.2567, -128.6, -72.7273]
        for i in range(0, len(results20to30)):
            self.assertAlmostEqual((results20to30[i]), cci.get_value(i + 19), 4)
