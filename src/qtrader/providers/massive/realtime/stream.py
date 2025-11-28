# src/qtrader/providers/massive/realtime/stream.py

from .websocket import MassiveWebSocket

class MassiveStream:
    """
    Minimal realtime stream for Massive data.
    """

    def __init__(self, api_key: str):
        self.ws = MassiveWebSocket(api_key)

    def subscribe_trades(self, tickers):
        """
        Subscribe to trade events for a list of tickers.
        """
        channels = [f"trades:{ticker}" for ticker in tickers]
        self.ws.subscribe(channels)

    def subscribe_quotes(self, tickers):
        """
        Subscribe to quote events for a list of tickers.
        """
        channels = [f"quotes:{ticker}" for ticker in tickers]
        self.ws.subscribe(channels)

    def start(self, on_message):
        """
        Start the websocket feed and process messages with on_message callback.
        """
        self.ws.run(on_message)
