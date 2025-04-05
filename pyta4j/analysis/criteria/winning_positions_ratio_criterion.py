from pyta4j.analysis.criteria.analysis_criterion import AnalysisCriterion

class WinningPositionsRatioCriterion(AnalysisCriterion):
    def calculate(self, series, trading_record):
        positions = trading_record.get_positions()
        if not positions:
            return 0
        winning_positions = sum(1 for pos in positions if pos.get_profit() > 0)
        total_positions = len(positions)
        return winning_positions / total_positions if total_positions > 0 else 0