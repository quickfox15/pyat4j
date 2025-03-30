from abc import ABC, abstractmethod


class Rule(ABC):

    @abstractmethod
    def is_satisfied(self, index, trading_record=None)->bool:
        raise NotImplementedError("Subclasses must implement is_satisfied")
    
    def or_(self, other_rule):
        return OrRule(self, other_rule)

    def and_(self, other_rule):
        return AndRule(self, other_rule)

    # Add operator overloading
    def __and__(self, other_rule):
        """Combine two rules with logical AND using &."""
        return AndRule(self, other_rule)

    def __or__(self, other_rule):
        """Combine two rules with logical OR using |."""
        return OrRule(self, other_rule)

    def __invert__(self):
        """Negate a rule using ~."""
        return NotRule(self)
    
class OrRule(Rule):
    def __init__(self, rule1, rule2):
        self.rule1 = rule1
        self.rule2 = rule2

    def is_satisfied(self, index, trading_record=None):
        return self.rule1.is_satisfied(index,trading_record) or self.rule2.is_satisfied(index,trading_record)

class AndRule(Rule):
    def __init__(self, rule1, rule2):
        self.rule1 = rule1
        self.rule2 = rule2

    def is_satisfied(self, index, trading_record=None):
        return self.rule1.is_satisfied(index,trading_record) and self.rule2.is_satisfied(index,trading_record)
    
class NotRule(Rule):
    def __init__(self, rule_to_negate):
        self.rule_to_negate = rule_to_negate

    def is_satisfied(self, index, trading_record=None):
        return not self.rule_to_negate.is_satisfied(index,trading_record)