import os
import time
import pandas as pd
import numpy as np
import tushare as ts
import config
import crawler_simple
from PositionFile import PositionFile  # pyright: ignore[reportImplicitRelativeImport]
from QuoteSource import QuoteSource  # pyright: ignore[reportImplicitRelativeImport]
from Portfolio import Portfolio  # pyright: ignore[reportImplicitRelativeImport]

start = time.perf_counter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '20251212.csv')

pos = PositionFile(CSV_PATH)
df = pos.df
# print(df)

token = config.TOKEN
data = '20251212'
before = '20251101'
pos1 = QuoteSource(token, data,before)
df1 = pos1.df
# print(df1)
raw2 = crawler_simple.get_constituents("000009")  # 爬虫：下载+解析，返回 code 列

raw2['code'] = raw2['code'].apply(pos.add_suffix)
# print(raw2)
pos2 = Portfolio(raw2,df)
df2= pos2.df
# print(df2)
df2.dropna(inplace=True)
df2.reset_index(drop=True, inplace=True)

pos3 = Portfolio(df2,df1)
df3= pos3.df
# print(df2)

df3.close = df3.apply(pos1.is_close, axis=1)

df3['market_value'] = df3.hold_vol * df3.close
m = df3['market_value'].sum()
print(f"380中证总市值: {m:.2f} 元")
print(f"耗时: {time.perf_counter() - start:.2f} 秒")
