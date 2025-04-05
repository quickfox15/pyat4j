from pyta4j.cost.cost_model import CostModel

class ZeroCostModel(CostModel):

    def calculate(self, position, final_index=None):
        return 0

    def calculate_price_amount(self, price, amount):
        return 0
