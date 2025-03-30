from pyta4j.rules.rule import Rule


class TrueRule(Rule):
    def is_satisfied(self, index, trading_record=None):
        return True

class FalseRule(Rule):
    def is_satisfied(self, index, trading_record=None):
        return False

# Test the operators
rule1 = TrueRule() & FalseRule()
print(rule1.is_satisfied(0))  # False (True AND False)

rule2 = TrueRule() | FalseRule()
print(rule2.is_satisfied(0))  # True (True OR False)

rule3 = ~TrueRule()
print(rule3.is_satisfied(0))  # False (NOT True)