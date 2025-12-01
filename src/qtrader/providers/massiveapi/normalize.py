# src/qtrader/providers/massiveapi/normalize.py

from datetime import datetime
import pandas as pd

def normalize_aggs(aggs, ticker=None):
    """
    Convert Massive aggregate bars into a pandas DataFrame.
    """
    rows = []
    for a in aggs:
        rows.append({
            "datetime": datetime.utcfromtimestamp(a.timestamp / 1000),
            "ticker": ticker,
            "open": a.open,
            "high": a.high,
            "low": a.low,
            "close": a.close,
            "volume": a.volume,
        })

    return pd.DataFrame(rows)
