from decimal import Decimal
from pyta4j.cost.cost_model import CostModel
from pyta4j.core.position import Position

class LinearTransactionCostModel(CostModel):

    def __init__(self,feePerPosition:Decimal):
        self.feePerPosition = feePerPosition
        
    def calculate(self, position:Position, final_index=None)-> Decimal:
        entryTrade = position.entry
        if entryTrade is not None:
            # transaction costs of entry trade
            totalPositionCost = entryTrade.cost
            if position.exit is not None:
                totalPositionCost = totalPositionCost + position.exit.cost
            return totalPositionCost
        
        return None

 
    def calculate_price_amount(self, price:Decimal, amount:Decimal)-> Decimal:
        return self.feePerPosition * price * amount