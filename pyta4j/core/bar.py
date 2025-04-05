class Bar:
    def __init__(self, duration, end_time, begin_time=None):
        self.duration = duration
        self.end_time = end_time
        self.begin_time = begin_time or (end_time - duration)
        self.trades = 0
        self.volume = 0
        self.open_price = None
        self.high_price = None
        self.low_price = None
        self.close_price = None
        self.amount = None
 
    def in_period(self, timestamp):
        start_time = self.end_time - self.duration
        return start_time <= timestamp < self.end_time

    def add_trade(self, volume, price):
        self.trades += 1
        self.volume += volume
        if self.open_price is None:
            self.open_price = price
        self.high_price = max(self.high_price or price, price)
        self.low_price = min(self.low_price or price, price)
        self.close_price = price

    def __eq__(self, other):
        if not isinstance(other, Bar):
            return NotImplemented
        return (
            self.duration == other.duration and
            self.end_time == other.end_time and
            self.open_price == other.open_price and
            self.high_price == other.high_price and
            self.low_price == other.low_price and
            self.close_price == other.close_price and
            self.volume == other.volume and
            self.trades == other.trades
        )

    def __hash__(self):
        return hash((
            self.duration,
            self.end_time,
            self.open_price,
            self.high_price,
            self.low_price,
            self.close_price,
            self.volume,
            self.trades
        ))

    def __str__(self):
        return (f"Bar(duration={self.duration}, end_time={self.end_time}, begin_time={self.begin_time} "
                f"open={self.open_price}, high={self.high_price}, low={self.low_price}, "
                f"close={self.close_price}, volume={self.volume}, trades={self.trades})")

    def __repr__(self):
        return self.__str__()