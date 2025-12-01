from datetime import datetime

def normalize_aggs(aggs):
    """
    Convert Massive Agg objects to dicts with datetime and readable keys.
    """
    normalized = []
    for a in aggs:
        normalized.append({
            "datetime": datetime.utcfromtimestamp(a.timestamp / 1000),
            "open": a.open,
            "high": a.high,
            "low": a.low,
            "close": a.close,
            "volume": a.volume,
        })
    return normalized