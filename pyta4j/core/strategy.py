class Strategy:
    def __init__(self, buying_rule, selling_rule):
        self.buying_rule = buying_rule
        self.selling_rule = selling_rule

    def should_enter(self, index, trading_record):
        """Check if the buying rule is satisfied at the given index."""
        return self.buying_rule.is_satisfied(index, trading_record)

    def should_exit(self, index, trading_record):
        """Check if the selling rule is satisfied at the given index."""
        return self.selling_rule.is_satisfied(index, trading_record)
    
    def should_operate(self, index, trading_record):
        position = trading_record.current_position
        if position.is_new():
            return self.should_enter(index, trading_record)
        elif position.is_opened():
            return self.should_exit(index, trading_record)
        return False
