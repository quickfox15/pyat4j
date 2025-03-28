from decimal import Decimal
from pyta4j.cost.cost_model import CostModel

class ZeroCostModel(CostModel):

    def calculate(self, position, final_index=None)-> Decimal:
        return Decimal('0')

    def calculate_price_amount(self, price:Decimal, amount:Decimal)-> Decimal:
        return Decimal('0')
