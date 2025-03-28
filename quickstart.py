from pyta4j.analysis.criteria.pnl.gross_return_criterion import GrossReturnCriterion
from pyta4j.analysis.criteria.return_over_max_drawdown_criterion import ReturnOverMaxDrawdownCriterion
from pyta4j.analysis.criteria.versus_buy_and_hold_criterion import VersusBuyAndHoldCriterion
from pyta4j.analysis.criteria.winning_positions_ratio_criterion import WinningPositionsRatioCriterion
from pyta4j.core.bar_series_manager import BarSeriesManager
from pyta4j.core.strategy import Strategy
from pyta4j.indicators.helpers.close_price_indicator import ClosePriceIndicator
from pyta4j.indicators.sma_indicator import SMAIndicator
from pyta4j.rules.crossed_up_indicator_rule import CrossedUpIndicatorRule
from pyta4j.rules.crossed_down_indicator_rule import CrossedDownIndicatorRule
from pyta4j.rules.stop_gain_rule import StopGainRule
from pyta4j.rules.stop_loss_rule import StopLossRule
from decimal import getcontext

from tests.loaders.csv_trades_loader import CsvTradesLoader
getcontext().prec = 28  # Match or exceed Java’s precision

def main():
    series = CsvTradesLoader.load_bitstamp_series()
    first_close_price = series.get_bar(0).close_price
    print(f"First close price: {first_close_price}")
    close_price = ClosePriceIndicator(series)
    print(f"First close price matches indicator: {first_close_price == close_price.get_value(0)}")
    short_sma = SMAIndicator(close_price, 5)
    print(f"5-bars-SMA value at the 42nd index: {short_sma.get_value(42)}")
    long_sma = SMAIndicator(close_price, 30)
    print(f"30-bars-SMA value at the 42nd index: {long_sma.get_value(42)}")
    buying_rule = CrossedUpIndicatorRule(short_sma, long_sma).or_(CrossedDownIndicatorRule(close_price, 800))
    print(f"Should buy at 42? {buying_rule.is_satisfied(42)}")

    selling_rule = CrossedDownIndicatorRule(short_sma, long_sma).or_(StopLossRule(close_price, 3)).or_(StopGainRule(close_price, 2))

    # Add the new strategy execution logic
    strategy = Strategy(buying_rule, selling_rule)
    series_manager = BarSeriesManager(series)
    trading_record = series_manager.run(strategy)
    print(f"Number of positions for our strategy: {len(trading_record.get_positions())}")

    # Analysis
    winning_positions_ratio = WinningPositionsRatioCriterion()
    print(f"Winning positions ratio: {winning_positions_ratio.calculate(series, trading_record)}")

    romad = ReturnOverMaxDrawdownCriterion()
    print(f"Return over Max Drawdown: {romad.calculate(series, trading_record)}")

    gross_return = GrossReturnCriterion()
    print(f"Gross return: {gross_return.calculate(series, trading_record)}")

    vs_buy_and_hold = VersusBuyAndHoldCriterion(GrossReturnCriterion())
    print(f"Our return vs buy-and-hold return: {vs_buy_and_hold.calculate(series, trading_record)}")

if __name__ == "__main__":
    main()