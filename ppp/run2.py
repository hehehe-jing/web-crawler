import os
import time
import config  # pyright: ignore[reportImplicitRelativeImport]
import crawler_simple  # pyright: ignore[reportImplicitRelativeImport]
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
# print(snapshot)

cons_codes = crawler_simple.get_constituents("000009")  # 爬虫：下载+解析，返回 code 列
cons_codes['code'] = cons_codes['code'].apply(position.add_suffix)
# print(cons_codes)

pos2 = Portfolio(cons_codes,holdings)
book1= pos2.df
book1.dropna(inplace=True)
book1.reset_index(drop=True, inplace=True)
# print(book1)

pos3 = Portfolio(book1,snapshot)
book2= pos3.df
book2.close = book2.apply(quotes.last_close, axis=1)
# print(book2)

print(f"380中证总市值: {Portfolio.return_market_value(book2):.2f} 元")
print(f"耗时: {time.perf_counter() - start:.2f} 秒")
