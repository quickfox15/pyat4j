from pyta4j.rules.rule import Rule

class IsRisingRule(Rule):
    def __init__(self,indicator,bar_count,min_strenght=1.0):
        super().__init__()
        self.indicator = indicator
        self.bar_count = bar_count
        self.min_strenght = min_strenght
    
    def is_satisfied(self, index, trading_record=None):
        min_strenght = min(self.min_strenght, 0.99)

        count = 0
        for i in range(max(0, index - self.bar_count + 1), index + 1):
            if self.indicator.get_value(i) > self.indicator.get_value(max(0, i - 1)):
                count += 1

        ratio = count / float(self.bar_count)
        satisfied = ratio >= min_strenght
        # Optionally: log or debug here
        # print(f"index={index}, count={count}, ratio={ratio}, satisfied={satisfied}")

        return satisfied
