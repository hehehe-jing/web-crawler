import os
import time
import config  # pyright: ignore[reportImplicitRelativeImport]
from PositionFile import PositionFile  # pyright: ignore[reportImplicitRelativeImport]
from QuoteSource import QuoteSource  # pyright: ignore[reportImplicitRelativeImport]
from Portfolio import Portfolio  # pyright: ignore[reportImplicitRelativeImport]

start = time.perf_counter()

token = config.TOKEN
start_date = config.START_DATE
before_date = config.BEFORE_DATE
CSV_PATH = config.CSV_PATH

position = PositionFile(CSV_PATH)
holdings = position.df
# print(holdings)

quotes = QuoteSource(token, start_date,before_date)
snapshot = quotes.df
pct_chg = quotes.pct_chg
# print(snapshot)



pos2 = Portfolio(holdings,snapshot)
book1= pos2.df
# print(snapshot)

book1.close = book1.apply(quotes.last_close, axis=1)
book1['pre_close'] = book1['pre_close'].fillna(book1['close'])
book1['change'] = book1['change'].fillna(0)
# print(book1)

ret_pct = Portfolio.return_ret_pct(book1)
excess_pct = ret_pct-pct_chg

print(f"\n今日总市值: {Portfolio.return_market_value(book1):.2f} 元")
print(f"昨日总市值: {Portfolio.return_market_value_pre(book1):.2f} 元\n")
print(f"按照（今日总市值-昨日总市值计算的）   今日收益额: {Portfolio.return_gain_by_diff(book1):.2f} 元")
print(f"按照（（close-pre_close）*hold_vol）.sum()计算的  今日收益额为: {Portfolio.return_gain_by_pre_close(book1):.2f} 元")
print(f"按照（change*hold_vol）.sum()计算的  今日收益额: {Portfolio.return_gain_by_change(book1):.2f} 元\n")
print(f"今日收益率为: {Portfolio.return_ret_pct(book1):.4f} %")
print(f"沪深300指数在{start_date}的涨跌幅为: {pct_chg:.4f}%")
print(f"今日超额收益率为: {excess_pct:.4f} %")
print(f"耗时: {time.perf_counter() - start:.2f} 秒")
