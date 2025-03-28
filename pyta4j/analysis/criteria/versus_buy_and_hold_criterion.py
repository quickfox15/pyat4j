from decimal import Decimal

from pyta4j.analysis.criteria.analysis_criterion import AnalysisCriterion
from pyta4j.core.trading_record import TradingRecord


class VersusBuyAndHoldCriterion(AnalysisCriterion):
    def __init__(self, return_criterion):
        self.return_criterion = return_criterion

    def calculate(self, series, trading_record):
        #def operate(self, index, price, amount):
        fake_record = TradingRecord()
        fake_record.enter(0,series.bars[0].close_price,series.bars[0].volume)
        fake_record.exit(len(series.bars)-1,series.bars[-1].close_price,series.bars[-1].volume)
        return self.return_criterion.calculate(series, trading_record) / self.return_criterion.calculate(series, fake_record)
