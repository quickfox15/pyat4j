import unittest

from pyta4j.indicators.statistics.standard_deviation_indicator import StandardDeviationIndicator
from tests.utils.trading_test_helpers import populate_bar_series
from pyta4j.indicators.sma_indicator import SMAIndicator
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator

from pyta4j.indicators.bollinger.bollinger_bands_middle_indicator import BollingerBandsMiddleIndicator
from pyta4j.indicators.bollinger.bollinger_bands_upper_indicator import BollingerBandsUpperIndicator

class TestBollingerBandsUpperIndicator(unittest.TestCase):

    def setUp(self):
        data = [1, 2, 3, 4, 3, 4, 5, 4, 3, 3, 4, 3, 2]
        self.series = populate_bar_series(data)
        self.bar_count = 3
        self.close_price = ClosePriceIndicator(self.series)
        self.sma = SMAIndicator(self.close_price, self.bar_count)
        
    def test_bollinger_bands_upper_using_sma_and_standard_deviation(self):
        bbm_sma = BollingerBandsMiddleIndicator(self.sma)
        standard_deviation = StandardDeviationIndicator(self.close_price, self.bar_count)
        bbu_sma = BollingerBandsUpperIndicator(bbm_sma, standard_deviation)

        self.assertAlmostEqual(2, bbu_sma.k)

        self.assertAlmostEqual((1), bbu_sma.get_value(0))
        self.assertAlmostEqual((2.5), bbu_sma.get_value(1))
        self.assertAlmostEqual((3.633), bbu_sma.get_value(2),3)
        self.assertAlmostEqual((4.633), bbu_sma.get_value(3),3)
        self.assertAlmostEqual((4.2761), bbu_sma.get_value(4),3)
        self.assertAlmostEqual((4.6094), bbu_sma.get_value(5),3)
        self.assertAlmostEqual((5.633), bbu_sma.get_value(6),3)
        self.assertAlmostEqual((5.2761), bbu_sma.get_value(7),3)
        self.assertAlmostEqual((5.633), bbu_sma.get_value(8),3)
        self.assertAlmostEqual((4.2761), bbu_sma.get_value(9),3)
        
        bbuSMAwithK = BollingerBandsUpperIndicator(bbm_sma, standard_deviation, 1.5)
        self.assertAlmostEqual(1.5, bbuSMAwithK.k)
        self.assertAlmostEqual((1), bbuSMAwithK.get_value(0),3)
        self.assertAlmostEqual((2.25), bbuSMAwithK.get_value(1),3)
        self.assertAlmostEqual((3.2247), bbuSMAwithK.get_value(2),3)
        self.assertAlmostEqual((4.2247), bbuSMAwithK.get_value(3),3)
        self.assertAlmostEqual((4.0404), bbuSMAwithK.get_value(4),3)
        self.assertAlmostEqual((4.3737), bbuSMAwithK.get_value(5),3)
        self.assertAlmostEqual((5.2247), bbuSMAwithK.get_value(6),3)
        self.assertAlmostEqual((5.0404), bbuSMAwithK.get_value(7),3)
        self.assertAlmostEqual((5.2247), bbuSMAwithK.get_value(8),3) 
        self.assertAlmostEqual((4.0404), bbuSMAwithK.get_value(9),3)
