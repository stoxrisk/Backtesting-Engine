import Strategy
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

def runstrategy():
    args = parse_args()

bullish_engulfing = Strategy.BullishEngulfing()

cerebro = bt.Cerebro()
cerebro.addstrategy(bullish_engulfing)

data0 = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime(2011, 1, 1),
                                  todate=datetime(2018, 12, 31))
cerebro.adddata(data0)

cerebro.run()
cerebro.plot()

