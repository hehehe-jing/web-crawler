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
pct_chg = pos1.pct_chg
merged = df.merge(df1, on='code', how='left')


merged.close = merged.apply(pos1.is_close, axis=1)
# pre_close 用 close 填（停牌当天收益为 0）
merged['pre_close'] = merged['pre_close'].fillna(merged['close'])

# change 也补 0（或者用 close - pre_close）
merged['change'] = merged['change'].fillna(0)


merged['market_value'] = merged.hold_vol * merged.close
merged['market_value1'] = merged.hold_vol * merged.pre_close
merged['market_value2'] = merged.hold_vol * merged.change
m = merged['market_value'].sum()
m1 = merged['market_value1'].sum()
m2 = merged['market_value'].sum() - merged['market_value1'].sum()
m3 = merged['market_value2'].sum()
m4 = (m2/m1)*100
m5 = m4-pct_chg
m6 = m-m1
print(f"\n今日总市值: {m:.2f} 元")
print(f"昨日总市值: {m1:.2f} 元\n")
print(f"按照（今日总市值-昨日总市值计算的）   今日收益额: {m6:.2f} 元")
print(f"按照（（close-pre_close）*hold_vol）.sum()计算的  今日收益额为: {m2:.2f} 元")
print(f"按照（change*hold_vol）.sum()计算的  今日收益额: {m3:.2f} 元\n")
print(f"今日收益率为: {m4:.4f} %")
print(f"沪深300指数在{data}的涨跌幅为: {pct_chg:.4f}%")
print(f"今日超额收益率为: {m5:.4f} %")
print(f"耗时: {time.perf_counter() - start:.2f} 秒")
