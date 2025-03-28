from abc import ABC, abstractmethod
from decimal import Decimal

class CostModel(ABC):

    @abstractmethod
    def calculate(self, position, final_index=None)-> Decimal:
        raise NotImplementedError('Subclasses must implement calculate')
    @abstractmethod
    def calculate_price_amount(self, price:Decimal, amount:Decimal)-> Decimal:
        raise NotImplementedError('Subclasses must implement calculate')
