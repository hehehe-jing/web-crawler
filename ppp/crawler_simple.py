# -*- coding: utf-8 -*-
import io
import time

import pandas as pd
import requests


def get_constituents(code="000009"):
    """下载并解析指数成份股，返回带 code 列的 DataFrame。"""
    url = ("https://oss-ch.csindex.com.cn/static/html/csindex/public/uploads/"
           f"file/autofile/cons/{code}cons.xls")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
               "Referer": "https://www.csindex.com.cn/"}

    for attempt in range(1, 4):
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            print(f"下载成功（第 {attempt} 次尝试）")
            break
        except requests.RequestException as e:
            print(f"第 {attempt} 次失败: {e}")
            time.sleep(2)
    else:
        raise RuntimeError("下载失败，请检查网络")

    # 不落盘，直接在内存里解析，避免本地文件被 Excel 占用导致写入失败
    df = pd.read_excel(io.BytesIO(resp.content), engine="xlrd", dtype=str)
    cons = df["成份券代码Constituent Code"].astype(str)
    return cons.to_frame(name="code")


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sse380_cons.csv")
    get_constituents().to_csv(out, index=False, encoding="utf-8-sig")
    print("已保存", out)
