import os
import time
import pandas as pd
import numpy as np
import tushare as ts
from PositionFile import PositionFile  # pyright: ignore[reportImplicitRelativeImport]
from QuoteSource import QuoteSource  # pyright: ignore[reportImplicitRelativeImport]
from Portfolio import Portfolio  # pyright: ignore[reportImplicitRelativeImport]

start = time.perf_counter()

# -*- coding: utf-8 -*-
URL = ("https://oss-ch.csindex.com.cn/static/html/csindex/public/uploads/"
       "file/autofile/cons/{code}cons.xls")          # 换 code 即换指数

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'c31cbd87d1784beb8589f9c4ee4ff7a4.csv')

pos = PositionFile(CSV_PATH)
df = pos.df
# print(df)

token = '4ea92729194a9a3a60f9c75dd60eb9a854622f774030aed003a3e329'
data = '20251212'
before = '20250101'
pos1 = QuoteSource(token, data,before)
df1 = pos1.df
# print(df1)
raw = pd.read_excel(URL.format(code="000009"), engine="xlrd", dtype=str)  # 下载+解析，一步
raw2 = raw[["成份券代码Constituent Code"]].copy()
raw2 = raw2.rename(columns={"成份券代码Constituent Code": "code"})# pyright: ignore[reportCallIssue]

raw2.code = raw2.code.apply(pos.add_suffix)
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
print(f"总市值: {m:.2f} 元")
print(f"耗时: {time.perf_counter() - start:.2f} 秒")
