# src/qtrader/providers/massiveapi/realtime/stream.py

from typing import Union, Iterable
from .websocket import MassiveWebSocket


class MassiveStream:
    """
    Minimal realtime stream wrapper for Massive data.
    """

    def __init__(self, api_key: str):
        self.ws = MassiveWebSocket(api_key)

    def _normalize_tickers(self, tickers: Union[str, Iterable[str]]) -> list[str]:
        """
        Always return tickers as a list.
        """
        if isinstance(tickers, str):
            return [tickers]
        return list(tickers)

    def subscribe_trades(self, tickers: Union[str, Iterable[str]]):
        """
        Subscribe to trade events for one or more tickers.
        """
        tickers = self._normalize_tickers(tickers)
        channels = [f"trades:{t}" for t in tickers]  # colon format here, sanitized later
        self.ws.subscribe(channels)

    def subscribe_quotes(self, tickers: Union[str, Iterable[str]]):
        """
        Subscribe to quote events for one or more tickers.
        """
        tickers = self._normalize_tickers(tickers)
        channels = [f"quotes:{t}" for t in tickers]
        self.ws.subscribe(channels)

    def start(self, on_message):
        """
        Start the websocket feed.
        """
        self.ws.run(on_message)
