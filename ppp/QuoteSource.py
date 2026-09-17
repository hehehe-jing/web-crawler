import os
import time
import pandas as pd
import numpy as np
import tushare as ts
import requests


class QuoteSource:

    def __init__(self, token, trade_date, before):
        ts.set_token(token)
        self.pro = ts.pro_api()
        self.trade_date = trade_date
        self.before = before
        self.cache = {}

        df1 = self.pro.daily(trade_date=trade_date)
        df = df1[['ts_code', 'close', 'pre_close', 'change']].copy()
        df = df.rename(columns={'ts_code': 'code'})  # pyright: ignore[reportUnknownMemberType, reportCallIssue]

        end = f'{self.trade_date[:4]}-{self.trade_date[4:6]}-{self.trade_date[6:]}'
        start = f'{self.before[:4]}-{self.before[4:6]}-{self.before[6:]}'
        rows = \
        requests.get(f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh000300,day,{start},{end},30,').json()[
            'data']['sh000300']['day']
        prev, cur = float(rows[-2][2]), float(rows[-1][2])
        pct_chg = (cur - prev) / prev * 100

        self.df = df
        self.pct_chg = pct_chg

    def is_close(self, row):  # 去掉 @staticmethod
        if not pd.isna(row['close']):
            return row['close']

        hist = self.pro.daily(ts_code=row['code'], start_date=self.before, end_date=self.trade_date)

        if hist.empty:
            print(f"{row['code']} 在该区间内无数据")
            raise ValueError(f"{row['code']} 无法取得收盘价")

        last = hist.sort_values('trade_date', ascending=False).iloc[0]
        print(f"{row['code']} 停牌前最后交易日: {last['trade_date']}，已正确填充")
        return last['close']
