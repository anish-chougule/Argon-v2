import pandas as pd
import numpy as np
import yfinance as yf
from backtesting import Backtest

from apps.backtest_strategies import *
from apps.strategy_optimizer import *

class Argon():

    model = {"MACD" : MacdCross,
         "RSI"  : RsiBreakout,
         "SMA"   : SmaCross}

    def __init__(self) -> None:
        self.cash     = 100000
        self.ticker   = "TSLA"            
        self.start    = "2022-03-01"      
        self.end      = "2023-03-01"
        self.interval = "1h"
        self.id       = "MACD"
        self.optimize = False
        self.vars_set = False

    def setModel(self, cash:int, id:str, ticker:str, optimize:bool):
        self.cash     = cash
        self.id       = id.upper()
        self.ticker   = ticker
        self.optimize = optimize

        self.df = yf.download(self.ticker, start=self.start, end=self.end, interval=self.interval, progress=False)
        if self.df.empty:
            raise ValueError('Unknow ticker symbol')
        
        try:
            _temp = self.model[self.id]
        except KeyError:
            raise KeyError('Unknown Model. Select from: MACD, RSI, SMA')
        
        self.vars_set = True



    def getStats(self):

        if not self.vars_set:
            raise Exception('Set variables first...')

        df = self.df[["Open", "High", "Low", "Close", "Volume"]]
        df.dropna(inplace=True)
        self.bt = Backtest(df, self.model[self.id],
                cash=self.cash, trade_on_close=False, exclusive_orders=True)

        if self.optimize:
            self.stats = optimize_strategy(self.bt, self.id, max="Equity Final [$]")            
        else:
            self.stats = self.bt.run()

        rounded_stats = self.stats
        for item, value in enumerate(rounded_stats):
            if type(value) is float:
                rounded_stats[item] = np.round(value, 2)

        return rounded_stats

    def plot(self, stats):        
        self.bt.plot(results=stats, open_browser=True)
