from pyta4j.cost.cost_model import CostModel
from pyta4j.core.trade import TradeType,Position

class LinearBorrowingCostModel(CostModel):

    # feePerPeriod the coefficient (e.g. 0.0001 for 1bp per period)
    def __init__(self,feePerPeriod):
        self.feePerPeriod = feePerPeriod
    
    def calculate(self, position:Position, final_index=None):

        if final_index is None:
            final_index = position.get_final_index()

        entryTrade = position.entry
        exitTrade = position.exit
        borrowingCost = 0
        #borrowing costs apply for short positions only
        if entryTrade is not None and entryTrade.trade_type == TradeType.SELL and entryTrade.amount is not None:
            tradingPeriods = 0
            if position.is_closed():
                tradingPeriods = exitTrade.index - entryTrade.index
            elif position.is_opened():
                tradingPeriods = final_index - entryTrade.index
            borrowingCost = self.get_holding_cost_for_periods(tradingPeriods, position.entry.get_value())

        return borrowingCost
 

    def calculate_price_amount(self, price, amount):
        return 0

    def get_holding_cost_for_periods(self, trading_periods:int, traded_value):
        return traded_value * trading_periods * self.feePerPeriod