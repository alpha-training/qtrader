# src/qtrader/providers/massive/historical/downloader.py

from .rest import MassiveHistoricalClient
import logging
from typing import List, Dict
import time

logger = logging.getLogger(__name__)


class MassiveHistoricalDownloader:
    """
    Bulk download historical data using MassiveHistoricalClient.
    """

    def __init__(self, client: MassiveHistoricalClient, sleep_sec: float = 0.1):
        self.client = client
        self.sleep_sec = sleep_sec

    def download_trades(self, symbols: List[str], start: str = None, end: str = None) -> Dict[str, List[Dict]]:
        """
        Download trades for multiple symbols.
        """
        results = {}
        for sym in symbols:
            try:
                trades = self.client.get_trades(sym, start=start, end=end)
                results[sym] = trades
                time.sleep(self.sleep_sec)  # avoid rate-limits
            except Exception as e:
                logger.exception("Error downloading trades for %s: %s", sym, e)
        return results

    def download_aggregates(self, symbols: List[str], interval: str = "1d", start: str = None, end: str = None) -> Dict[str, List[Dict]]:
        """
        Download OHLCV aggregates for multiple symbols.
        """
        results = {}
        for sym in symbols:
            try:
                aggs = self.client.get_aggregates(sym, interval=interval, start=start, end=end)
                results[sym] = aggs
                time.sleep(self.sleep_sec)
            except Exception as e:
                logger.exception("Error downloading aggregates for %s: %s", sym, e)
        return results
