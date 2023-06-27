"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/6/16 17:47
# @Author:Szeto YiZe
# @File:python_backtest_stock_strategy.py
# @Update:
"""

import yfinance as yf
import pandas as pd
import numpy as np

"""

# 下载股票数据
stock_data = yf.download("AAPL", start="2010-01-01", end="2021-06-11")

# 计算移动平均线
stock_data["SMA10"] = stock_data["Close"].rolling(window=10).mean()
stock_data["SMA50"] = stock_data["Close"].rolling(window=50).mean()

# 计算交易信号和持仓
stock_data["Signal"] = 0.0
stock_data["Signal"][10:] = np.where(stock_data["SMA10"][10:] > stock_data["SMA50"][10:], 1.0, 0.0)
stock_data["Position"] = stock_data["Signal"].diff()

# 回测策略
initial_capital = float(1000000.0)
positions = pd.DataFrame(index=stock_data.index).fillna(0.0)
portfolio = pd.DataFrame(index=stock_data.index).fillna(0.0)
portfolio["AAPL"] = 1000 * stock_data["Close"]
pos_diff = 1000 * stock_data["Position"]
positions["AAPL"] = pos_diff
portfolio["holdings"] = (positions.multiply(stock_data["Close"], axis=0)).sum(axis=1)
portfolio["cash"] = initial_capital - (pos_diff.multiply(stock_data["Close"], axis=0)).sum(axis=1).cumsum()
portfolio["total"] = portfolio["cash"] + portfolio["holdings"]
portfolio["returns"] = portfolio["total"].pct_change()

# 打印交易结果
print(portfolio.tail())

"""


def backtest_stock_strategy(ticker, short_window, long_window, initial_capital):
    # 下载股票数据
    stock_data = yf.download(ticker, start="2010-01-01", end="2021-06-11")

    # 计算移动平均线
    stock_data["SMA10"] = stock_data["Close"].rolling(window=short_window).mean()
    stock_data["SMA50"] = stock_data["Close"].rolling(window=long_window).mean()

    # 计算交易信号和持仓
    stock_data["Signal"] = 0.0
    stock_data["Signal"][short_window:] = np.where(
        stock_data["SMA10"][short_window:] > stock_data["SMA50"][short_window:], 1.0, 0.0)
    stock_data["Position"] = stock_data["Signal"].diff()

    # 回测策略
    positions = pd.DataFrame(index=stock_data.index).fillna(0.0)
    portfolio = pd.DataFrame(index=stock_data.index).fillna(0.0)
    portfolio[ticker] = initial_capital / stock_data["Close"][0] * stock_data["Close"]
    pos_diff = initial_capital * stock_data["Position"]
    positions[ticker] = pos_diff
    portfolio["holdings"] = (positions.multiply(stock_data["Close"], axis=0)).sum(axis=1)
    portfolio["cash"] = initial_capital - (pos_diff.multiply(stock_data["Close"], axis=0)).sum(axis=1).cumsum()
    portfolio["total"] = portfolio["cash"] + portfolio["holdings"]
    portfolio["returns"] = portfolio["total"].pct_change()

    # 打印交易结果
    print(portfolio.tail())
