import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind

class Strategy(bt.Strategy):

    def __init__(self):
        super().__init__()

    def next(self):
        super().next()

    def notify_order(self):
        super().notify_order()

    def notify_trade(self, trade):
        super().notify_trade(trade)


class BullishEngulfing(Strategy):

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        print(self.datas)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None


    def next(self):
        if self.order:
            return

        if not self.position:
            # Bullish Engulfing
            if (self.dataclose[0] >= self.dataclose[-1] and self.dataclose[0] >= self.dataopen[-1]) and (self. dataopen[0] <= self.dataopen[-1] and self.dataopen[0] <= self.dataopen[-1]):
                self.order = self.buy()
            
            # # Bearish Engulfing
            # elif (self.dataopen[0] >= self.dataclose[-1] and self.dataopen[0] >= self.dataopen[-1]) and (self. dataclose[0] <= self.dataopen[-1] and self.dataclose[0] <= self.dataopen[-1]):
            #     self.order = self.sell()
        else: 
            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()