from abc import ABC, abstractmethod

class CostModel(ABC):

    @abstractmethod
    def calculate(self, position, final_index=None):
        raise NotImplementedError('Subclasses must implement calculate')
    @abstractmethod
    def calculate_price_amount(self, price, amount):
        raise NotImplementedError('Subclasses must implement calculate')
