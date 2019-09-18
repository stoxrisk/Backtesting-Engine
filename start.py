import Strategy

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

from datetime import datetime


STARTING_CASH = 10000
SIZE = STARTING_CASH/4


def runstrategy():
    args = parse_args()

bullish_engulfing = Strategy.BullishEngulfing

cerebro = bt.Cerebro()
cerebro.addstrategy(bullish_engulfing)

data0 = bt.feeds.YahooFinanceData(dataname='SPXL', fromdate=datetime(2015, 1, 1),
                                  todate=datetime(2019, 8, 31))
cerebro.adddata(data0)

cerebro.broker.setcash(STARTING_CASH)
# cerebro.broker.slip_perc(slip_perc=0.0015)
cerebro.addsizer(bt.sizers.SizerFix, stake=50)

cerebro.run()
#getbroker()
print("End value is: " + str(cerebro.getbroker().get_value()))
cerebro.plot()
