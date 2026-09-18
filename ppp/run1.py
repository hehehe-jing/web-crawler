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
# print(snapshot)

pos2 = Portfolio(holdings,snapshot)
book= pos2.df
# print(book)

book.close = book.apply(quotes.last_close, axis=1)

print(f"总市值: {Portfolio.return_market_value(book):.2f} 元")
print(f"耗时: {time.perf_counter() - start:.2f} 秒")
