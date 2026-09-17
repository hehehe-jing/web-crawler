import os
import time
import pandas as pd
import numpy as np
import tushare as ts


class PositionFile:

    def __init__(self, path):
        df = pd.read_csv(path)
        if df['code'].duplicated().sum() > 0:
            df = df.groupby('code').agg({'hold_vol': 'sum'}).reset_index()
        if df['hold_vol'].isna().sum() > 0:
            df = df.fillna(0)

        df['code'] = df['code'].astype(str).str.strip().str.zfill(6)

        df['code'] = df['code'].apply(self.add_suffix)
        self.df = df

    @staticmethod
    def add_suffix(code):
        code = str(code).zfill(6)
        if code.startswith(('600', '601', '603', '605', '688', '689', '900')):
            return code + '.SH'
        elif code.startswith(('000', '001', '002', '003', '300', '301', '200')):
            return code + '.SZ'
        elif code.startswith(('8', '4')):
            return code + '.BJ'
        raise ValueError(f"股票代码 {code} 无法匹配交易所后缀，请检查持仓文件该行")