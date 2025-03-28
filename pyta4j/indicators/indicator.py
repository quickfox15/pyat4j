from abc import ABC, abstractmethod

class Indicator(ABC):

    @abstractmethod
    def get_value(self, index:int):
        raise NotImplementedError("Subclasses must implement get_value")