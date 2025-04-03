from datetime import datetime, timedelta, timezone
import unittest

from tests.utils.trading_test_helpers import populate_bar_series


class TestVarianceIndicator(unittest.TestCase):

    def setUp(self):
        data = [1, 2, 3, 4, 3, 4, 5, 4, 3, 0, 9]
        self.series = populate_bar_series(data)
    
