from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
# import backtrader as bt

# # We want to buy on bearish engulfing

# class SmaCross(bt.SignalStrategy):
#     def __init__(self):
#         sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
#         crossover = bt.ind.CrossOver(sma1, sma2)
#         self.signal_add(bt.SIGNAL_LONG, crossover)

# cerebro = bt.Cerebro()
# cerebro.addstrategy(SmaCross)

# data0 = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime(2011, 1, 1),
#                                   todate=datetime(2018, 12, 31))
# cerebro.adddata(data0)

# cerebro.run()
# cerebro.plot()


#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015, 2016 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################


import argparse

import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind


class BidAskCSV(btfeeds.GenericCSVData):
    linesoverride = True  # discard usual OHLC structure
    # datetime must be present and last
    lines = ('bid', 'ask', 'datetime')
    # datetime (always 1st) and then the desired order for
    params = (
        # (datetime, 0), # inherited from parent class
        ('bid', 1),  # default field pos 1
        ('ask', 2),  # default field pos 2
    )


class St(bt.Strategy):
    params = (('sma', False), ('period', 3))

    def __init__(self):
        if self.p.sma:
            self.sma = btind.SMA(self.data, period=self.p.period)

    def next(self):
        dtstr = self.data.datetime.datetime().isoformat()
        print(dir(self.data))
        txt = '%4d: %s - Bid %.4f - %.4f Ask' % (
            (len(self), dtstr, self.data.bid[0], self.data.ask[0]))

        if self.p.sma:
            txt += ' - SMA: %.4f' % self.sma[0]
        print(txt)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Bid/Ask Line Hierarchy',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('--data', '-d', action='store',
                        required=False, default='../../datas/bidask.csv',
                        help='data to add to the system')

    parser.add_argument('--dtformat', '-dt',
                        required=False, default='%m/%d/%Y %H:%M:%S',
                        help='Format of datetime in input')

    parser.add_argument('--sma', '-s', action='store_true',
                        required=False,
                        help='Add an SMA to the mix')

    parser.add_argument('--period', '-p', action='store',
                        required=False, default=5, type=int,
                        help='Period for the sma')

    return parser.parse_args()


def runstrategy():
    args = parse_args()

# python ./test.py -- 

cerebro = bt.Cerebro()
cerebro.addstrategy(St)

data0 = bt.feeds.YahooFinanceData(dataname='SPXL', fromdate=datetime(2017, 1, 1),
                                  todate=datetime(2019, 8, 31))
cerebro.adddata(data0)

cerebro.broker.setcash(100000.0)
cerebro.broker.slip_perc(slip_perc=0.0015)
cerebro.addsizer(bt.sizers.SizerFix, stake=20)

cerebro.run()
cerebro.plot()

