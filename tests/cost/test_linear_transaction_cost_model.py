from decimal import Decimal
import unittest

from pyta4j.core.position import Position
from pyta4j.core.trade import Trade, TradeType
from pyta4j.cost.linear_transaction_cost_model import LinearTransactionCostModel
from pyta4j.cost.zero_cost_model import ZeroCostModel

class TestLinearTransactionCostModel(unittest.TestCase):

    def setUp(self):
        self.transactionModel = LinearTransactionCostModel(Decimal('0.01'))

    def test_calculateSingleTradeCost(self):
        # Price - Amount calculation Test
        price = Decimal('100')
        amount = Decimal('2')
        cost = self.transactionModel.calculate_price_amount(price, amount)
        self.assertEqual(2, cost)

    def test_calculateBuyPosition(self):
        # Calculate the transaction costs of a closed long position
        holdingPeriod = 2
        entry = Trade.buy_at(0, Decimal('100'), Decimal('1'),self.transactionModel)
        exit = Trade.sell_at(holdingPeriod, Decimal('110'), Decimal('1'),self.transactionModel)
        print("Entry cost: ", entry.cost)
        # position = Position(entry, exit, self.transactionModel, ZeroCostModel())
        position = Position(TradeType.BUY, self.transactionModel, ZeroCostModel())
        position.entry = entry
        position.exit = exit

        costFromBuy = entry.cost
        costFromSell = exit.cost
        costsFromModel = self.transactionModel.calculate(position, holdingPeriod)

        self.assertEqual(costsFromModel, costFromBuy + costFromSell)
        self.assertEqual(costsFromModel, Decimal('2.1'))
        self.assertEqual(costFromBuy, Decimal('1'))
        self.assertEqual(costFromSell, Decimal('1.1'))

    