
from abc import ABC, abstractmethod

class AnalysisCriterion(ABC):
    @abstractmethod
    def calculate(self, series, trading_record):
        raise NotImplementedError("Subclasses must implement calculate")