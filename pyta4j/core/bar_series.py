import sys

class BarSeries:
    def __init__(self, name, bars=None):
        self.name = name
        self.bars = []
        self.series_end_index = - 1
        self.series_begin_index = -1
        self.maximum_bar_count = sys.maxsize
        self.removed_bars_count = 0
        self.constrained = False
        if bars is not None:
            for bar in bars:
                self.add_bar(bar)

    def add_bar(self, bar, replace=False):
        # Validate bar has a close price
        if not bar.close_price:
            raise ValueError("Bar has no close price")

        if self.bars:
            if replace:
                self.bars[-1] = bar
                return

            last_end_time = self.bars[-1].end_time

            # Only validate end_time ordering if bar.end_time is not None
            if bar.end_time is not None and last_end_time is not None:
                if bar.end_time <= last_end_time:
                    raise ValueError(
                        f"Cannot add a bar with end time: {bar.end_time} "
                        f"that is <= series end time: {last_end_time}"
                    )

        self.bars.append(bar)

        if self.series_begin_index == -1:
            self.series_begin_index = 0

        self.series_end_index += 1
        self.remove_exceeding_bars()

    def get_bar_count(self) -> int:
        return len(self.bars)
    
    def is_empty(self) -> bool:
        return self.get_bar_count() == 0

    def get_bar(self, index):
        internal_index = index - self.removed_bars_count
        if internal_index < 0 or internal_index >= len(self.bars):
            raise IndexError(f"Index {index} is out of bounds (removed: {self.removed_bars_count})")
        return self.bars[internal_index]
    
    #get last bar
    def get_last_bar(self):
        return self.bars[-1]
    
    #get first bar
    def get_first_bar(self):
        return self.bars[0]

    def get_name(self):
        return self.name

    def set_maximum_bar_count(self, maximum_bar_count):
        if self.constrained:
            raise ValueError("Cannot set a maximum bar count on a constrained bar series")
        if maximum_bar_count <= 0:
            raise ValueError("Maximum bar count must be strictly positive")
        self.maximum_bar_count = maximum_bar_count
        self.remove_exceeding_bars()

    #removes the N first bars which exceed the maximum bar count
    def remove_exceeding_bars(self):
        excess = len(self.bars) - self.maximum_bar_count
        if excess > 0:
            del self.bars[:excess]
            self.removed_bars_count += excess

    def get_series_period_description(self):
        if not self.bars:
            return "(empty)"
        return f"{self.bars[0].end_time} - {self.bars[-1].end_time}"