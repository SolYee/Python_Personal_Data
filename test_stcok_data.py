"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/4/24 17:48
# @Author:Szeto YiZe
# @File:test_stcok_data.py
# @Update:
"""
# # 导入相关模块
# import tushare as ts
# import pandas as pd
# import numpy as np
#
# # 获取股票数据
# stock_data = ts.get_hist_data('60')
#
# # 计算最低价
# low_price = np.min(stock_data['low'])
#
# # 定义买入价格区间
# buy_price_range = [low_price * 0.9, low_price * 1.1]
#
# # 盯盘
# while True:
#
#     # 获取实时价格
#     real_price = ts.get_realtime_quotes('60')['price'][0]
#     # 判断是否在买入价格区间
#     if real_price >= buy_price_range[0] and real_price <= buy_price_range[1]:
#         # 买入操作
#         print('买入操作')
#     break

import tushare as ts
import pandas as pd
import numpy as np


class StockTrader:
    def __init__(self, stock_code, buy_price_range):
        self.stock_code = stock_code
        self.buy_price_range = buy_price_range

    def get_low_price(self):
        stock_data = ts.get_hist_data(self.stock_code)
        return np.min(stock_data['low'])

    def watch_stock(self):
        while True:
            real_price = ts.get_realtime_quotes(self.stock_code)['price'][0]
            if real_price >= self.buy_price_range[0] and real_price <= self.buy_price_range[1]:
                self.buy_stock()
                break

    def buy_stock(self):
        # 买入操作
        print('买入操作')


if __name__ == '__main__':
    stock_code = '700'
    low_price = StockTrader(stock_code, None).get_low_price()
    buy_price_range = [low_price * 0.9, low_price * 1.1]
    stock_trader = StockTrader(stock_code, buy_price_range)
    stock_trader.watch_stock()

"""
首先定义了一个 `StockTrader` 类，用于封装股票交易相关操作。类的初始化方法 `__init__()` 接受两个参数，分别是股票代码 `stock_code` 和买入价格区间 `buy_price_range`。
其中，买入价格区间是一个列表，包含两个元素，表示最低买入价格和最高买入价格。

`get_low_price()` 方法用于获取股票的历史最低价格。在方法中，调用了 tushare 库的 `get_hist_data()` 函数获取股票的历史数据，然后使用 numpy 库的 `min()` 函数计算最低价格。

`watch_stock()` 方法是一个循环，用于监控股票价格。在循环中，首先使用 tushare 库的 `get_realtime_quotes()` 函数获取股票的实时价格，然后判断实时价格是否在买入价格区间内。
如果实时价格在买入价格区间内，则调用 `buy_stock()` 方法进行买入操作，并跳出循环。

`buy_stock()` 方法用于执行买入操作。在本示例中，只是简单地输出了一句话，实际操作需要根据实际情况进行实现。

最后，在主程序中创建了一个 `StockTrader` 对象，并调用 `watch_stock()` 方法进行监控。在初始化对象时，先调用 `get_low_price()` 方法获取历史最低价格，并根据历史最低价格计算买入价格区间。
"""
