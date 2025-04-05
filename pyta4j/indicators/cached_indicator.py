
from pyta4j.indicators.indicator import Indicator

class CachedIndicator(Indicator):

    def __init__(self):
        """Initialize the cached indicator with a source indicator."""
        super().__init__()
        self.results: list = []  # Cache for computed values
        self.highest_result_index:int = -1   # Tracks the highest computed index

    def get_value(self, index: int):
        """Retrieve the value at the given index, using cache if available."""
        # if index < 0:
        #     raise ValueError("Index cannot be negative")
        if index < 0:
            index = 0  # Treat negative indices as the earliest index
        
        # Extend the cache if the requested index is beyond current size
        if index >= len(self.results):
            self._increase_length_to(index)
        
        # If the value isn’t cached, compute and store it
        if self.results[index] is None:
            result = self.calculate(index)
            self.results[index] = result
        
        return self.results[index]

    def _increase_length_to(self, index: int):
        """Extend the cache list to accommodate the requested index."""
        if self.highest_result_index == -1:
            # Initial case: create a list up to the requested index
            self.results = [None] * (index + 1)
        else:
            # Extend the list with None values for new indices
            new_results_count = index - self.highest_result_index
            self.results.extend([None] * new_results_count)
        self.highest_result_index = index

    def calculate(self, index: int):
        """Abstract method to compute the value at the given index."""
        raise NotImplementedError("Subclasses must implement calculate method")