import numpy as np
import pandas as pd
import talib as ta

from backtesting.lib import crossover, TrailingStrategy


# Moving Averages Convergence Divergence Strategy
class MacdCross(TrailingStrategy):
    ###########
    _id = "macd"
    ###########

    fastperiod = 12
    slowperiod = 26
    signalperiod = 9

    def init(self):
        super().init()
        self.set_trailing_sl(3)

        high   = self.data.High
        low    = self.data.Low                
        close  = self.data.Close
        self.macd, self.signal = self.I(ta.MACD, close, self.fastperiod, self.slowperiod, self.signalperiod)[:2]
        self.atr = self.I(ta.ATR, high, low, close, 14)
        self.upperChannel = np.roll(close, 1) + 3*self.atr
        self.lowerChannel = np.roll(close, 1) - 3*self.atr

    def next(self):
        super().next()

        if crossover(self.macd, self.signal) or crossover(self.data.Close, self.upperChannel):
            self.buy(size = 0.6)

        elif crossover(self.signal, self.macd) or crossover(self.data.Close, self.lowerChannel):
            self.sell(size = 0.6)

# Relative Strengt Indicator Strategy
class RsiBreakout(TrailingStrategy):

    ###########
    _id = "rsi"
    ###########

    n1 = 40
    n2 = 200
    upper_bound = 60
    lower_bound = 40

    def init(self):
        super().init()
        self.set_trailing_sl(2.5)

        high = self.data.High
        low = self.data.Low                
        close = self.data.Close
        self.rsi = self.I(ta.RSI, close, self.n1)
        self.sma = self.I(ta.SMA, close, self.n2)
        self.atr = self.I(ta.ATR, high, low, close, 14)

    def next(self):
        super().next()
        close = self.data.Close[-1]

        if self.rsi[-1] < self.lower_bound and close<self.sma[-1] and not self.position:
            self.sl = self.data.Close[-1] - 2.5*self.atr[-1]
            self.buy(size=0.75, sl=self.sl)

        elif self.rsi[-1] > self.upper_bound and close>self.sma[-1] and not self.position:
            self.sl = self.data.Close[-1] + 2.5*self.atr[-1]
            self.sell(size=0.75, sl=self.sl)


# Moving Averages Strategy
class SmaCross(TrailingStrategy):
    
    #########
    _id = "ma"
    #########
    
    n1 = 40
    n2 = 200

    def init(self):
        super().init()
        self.set_trailing_sl(2.5)

        high = self.data.High
        low = self.data.Low                
        close = self.data.Close
        self.sma1 = self.I(ta.EMA, close, self.n1)
        self.sma2 = self.I(ta.EMA, close, self.n2)
        self.atr = self.I(ta.ATR, high, low, close, 14)
        self.upperChannel = np.roll(close, 1) + 3*self.atr
        self.lowerChannel = np.roll(close, 1) - 3*self.atr

    def next(self):
        super().next()
        for trade in self.trades:
            if self.data.index[-1] - trade.entry_time >= pd.Timedelta("8 days"):
                if trade.is_long:
                    trade.sl = max(trade.sl, self.data.Low[-1])
                else:
                    trade.sl = min(trade.sl, self.data.High[-1])

        if crossover(self.sma1, self.sma2) or crossover(self.data.Close, self.upperChannel):
            self.sl = self.data.Close[-1] - 2.5*self.atr[-1]
            self.buy(size=0.75, sl=self.sl)

        elif crossover(self.sma2, self.sma1) or crossover(self.data.Close, self.lowerChannel):
            self.sl = self.data.Close[-1] + 2.5*self.atr[-1]
            self.sell(size=0.75, sl=self.sl)

