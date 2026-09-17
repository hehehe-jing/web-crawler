import os
import time
import pandas as pd
import numpy as np
import tushare as ts
import config
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

pos2 = Portfolio(df,df1)
df2= pos2.df
# print(df2)

df2.close = df2.apply(pos1.is_close, axis=1)



# print(df2)
df2['market_value'] = df2.hold_vol * df2.close
m = df2['market_value'].sum()
print(f"总市值: {m:.2f} 元")
print(f"耗时: {time.perf_counter() - start:.2f} 秒")
