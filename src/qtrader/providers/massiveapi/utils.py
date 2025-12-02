# src/qtrader/providers/massive/utils.py

from datetime import datetime

def to_datetime(timestamp_ms: int) -> datetime:
    """
    Convert a UNIX timestamp in milliseconds to a Python datetime.
    """
    return datetime.utcfromtimestamp(timestamp_ms / 1000)