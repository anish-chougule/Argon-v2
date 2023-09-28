from backtesting import Backtest

_stats_labels = ["Start", "End", "Duration", "Exposure Time [%]", "Equity Final [$]",
                "Equity Peak [$]", "Return [%]", "Buy & Hold Return [%]", "Return (Ann.) [%]",
                "Volatility (Ann.) [%]", "Sharpe Ratio", "Sortino Ratio", "Calmar Ratio", "Max. Drawdown [%]"
                "Avg. Drawdown [%]", "Max. Drawdown Duration", "Avg. Drawdown Duration", "# Trades",
                "Win Rate [%]", "Best Trade [%]", "Worst Trade [%]", "Avg. Trade [%]", "Max. Trade Duration",
                "Avg. Trade Duration", "Profit Factor", "SQN"]

_id_labels = ["MACD", "RSI", "SMA"]

def optimize_strategy(bt:Backtest, id:_id_labels, max:_stats_labels = "Equity Final [$]"):
    
    if   id == "MACD":
        return optim_macd(bt, max)
    elif id == "RSI":
        return optim_rsi(bt, max)
    elif id == "SMA":
        return optim_sma(bt, max)
    else:
        pass

def optim_macd(bt:Backtest, max):
    stats = bt.optimize(fastperiod = range(12, 40, 2),
                        slowperiod = range(20, 60, 4),
                        signalperiod = range(5, 15, 2),
                        constraint = lambda p: p.slowperiod > p.fastperiod + 10 and p.fastperiod > p.signalperiod + 5,
                        maximize = max)
            
    return stats

def optim_rsi(bt:Backtest, max):
    stats = bt.optimize(n1 = range(10, 80, 4), 
                        n2 = range(40, 200, 5), 
                        maximize = max, 
                        constraint = lambda p: p.n1 < p.n2)

    return stats

def optim_sma(bt:Backtest, max):
    stats = bt.optimize(n1 = range(10, 50, 5), 
                        n2 = range(40, 200, 5), 
                        maximize = max, 
                        constraint = lambda p: p.n1 < p.n2)
    
    return stats

def get_stats_labels():
    return _stats_labels