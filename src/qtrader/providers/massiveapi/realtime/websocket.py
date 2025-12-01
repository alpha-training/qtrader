# src/qtrader/providers/massiveapi/realtime/websocket.py

from typing import Union, Iterable
from massive import WebSocketClient


class MassiveWebSocket:
    """
    Wrapper around Massive's WebSocketClient with subscription sanitisation.
    """

    def __init__(self, api_key: str):
        self.ws = WebSocketClient(api_key=api_key)

    def _sanitize_channel(self, channel: str) -> str:
        """
        Convert channels like 'trades:AAPL' → 'trades.AAPL' which is the
        correct Massive WS format and avoids the internal logging bug.
        """
        if ":" in channel:
            topic, sym = channel.split(":", 1)
            return f"{topic}.{sym}"
        return channel

    def subscribe(self, channels: Union[str, Iterable[str]]):
        """
        Subscribe to one or more channels.

        Parameters
        ----------
        channels : str or list[str]
            Channel strings like:
            - 'trades.AAPL'
            - 'quotes.MSFT'
        """
        if isinstance(channels, str):
            self.ws.subscribe(self._sanitize_channel(channels))
            return

        # channels is iterable
        for ch in channels:
            self.ws.subscribe(self._sanitize_channel(ch))

    def run(self, on_message):
        """
        Run the websocket and forward each event to the callback.

        Parameters
        ----------
        on_message : callable
            Function(event_dict)
        """
        self.ws.run(on_message)
