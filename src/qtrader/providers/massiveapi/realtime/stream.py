# src/qtrader/providers/massive/realtime/stream.py

from .websocket import MassiveWebSocket

class MassiveStream:
    """
    Minimal realtime stream for Massive data.
    """

    def __init__(self, api_key: str):
        self.ws = MassiveWebSocket(api_key)

    def _normalize_tickers(self, tickers):
        """
        Ensure tickers is a list even if a single string is provided.
        """
        if isinstance(tickers, str):
            return [tickers]
        return tickers

    def subscribe_trades(self, tickers):
        """
        Subscribe to trade events for one or more tickers.
        """
        tickers = self._normalize_tickers(tickers)
        channels = [f"trades:{ticker}" for ticker in tickers]
        self.ws.subscribe(channels)

    def subscribe_quotes(self, tickers):
        """
        Subscribe to quote events for one or more tickers.
        """
        tickers = self._normalize_tickers(tickers)
        channels = [f"quotes:{ticker}" for ticker in tickers]
        self.ws.subscribe(channels)

    def start(self, on_message):
        """
        Start the websocket feed and process messages with on_message callback.
        """
        self.ws.run(on_message)
