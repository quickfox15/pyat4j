from pyta4j.indicators.cached_indicator import CachedIndicator

class RecursiveCachedIndicator(CachedIndicator):

    def __init__(self):
        super().__init__()
        self.computed_up_to = -1  # Tracks the highest index with a computed value
        self.RECURSION_THRESHOLD = 100  # Threshold to switch to iterative computation

    def get_value(self, index: int):
        """Retrieve the value at the given index, avoiding deep recursion."""
        if index < 0:
            raise ValueError("Index cannot be negative")
        
        # Extend the list if necessary
        if index >= len(self.results):
            self._increase_length_to(index)
        
        # Return cached value if available
        if self.results[index] is not None:
            return self.results[index]
        
        # If the requested index is far ahead, compute iteratively
        if index - self.computed_up_to > self.RECURSION_THRESHOLD:
            for i in range(self.computed_up_to + 1, index + 1):
                self.results[i] = self.calculate(i)
            self.computed_up_to = index
        else:
            # Compute normally (limited recursion depth)
            self.results[index] = self.calculate(index)
            self.computed_up_to = index  # Update to the latest computed index
        
        return self.results[index]
