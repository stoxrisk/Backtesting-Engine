import Strategy

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import Config
from datetime import datetime

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Please provide a config file")
    exit(0)

config = Config()
config.loadConfigFile("\\configs\\%s" % filename)

def runstrategy():
    args = parse_args()

bullish_engulfing = Strategy.BullishEngulfing

cerebro = bt.Cerebro()
cerebro.addstrategy(bullish_engulfing)

data0 = bt.feeds.YahooFinanceData(dataname='SPXL', fromdate=datetime(2015, 1, 1),
                                  todate=datetime(2019, 8, 31))
cerebro.adddata(data0)

cerebro.broker.setcash(config.startingCash)
# cerebro.broker.slip_perc(slip_perc=0.0015)
cerebro.addsizer(bt.sizers.SizerFix, stake=50)

cerebro.run()
#getbroker()
print("End value is: " + str(cerebro.getbroker().get_value()))
cerebro.plot()
