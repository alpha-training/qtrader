# src/qtrader/providers/massive/historical/rest.py

from massive import RestClient
import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class MassiveHistoricalClient:
    """
    Minimal wrapper around Massive REST client for historical data.
    """

    def __init__(self, api_key: str, **rest_kwargs):
        """
        :param api_key: Massive API key
        :param rest_kwargs: optional kwargs for RestClient (like base_url, timeout)
        """
        self.api_key = api_key
        self._client = RestClient(api_key=api_key, **rest_kwargs)

    def get_snapshot(self, symbol: str, **kwargs) -> Dict[str, Any]:
        """
        Fetch a snapshot for a single symbol.
        """
        try:
            data = self._client.snapshot(symbol=symbol, **kwargs)
            return data
        except Exception as e:
            logger.exception("Error fetching snapshot for %s: %s", symbol, e)
            return {}

    def get_trades(self, symbol: str, start: str = None, end: str = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch historical trades for a symbol over a time range.
        """
        try:
            data = self._client.trades(symbol=symbol, start=start, end=end, **kwargs)
            return data
        except Exception as e:
            logger.exception("Error fetching trades for %s: %s", symbol, e)
            return []

    def get_aggregates(self, symbol: str, interval: str = "1d", start: str = None, end: str = None, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch OHLCV aggregates for a symbol over a time range.
        """
        try:
            data = self._client.aggs(symbol=symbol, interval=interval, start=start, end=end, **kwargs)
            return data
        except Exception as e:
            logger.exception("Error fetching aggregates for %s: %s", symbol, e)
            return []
