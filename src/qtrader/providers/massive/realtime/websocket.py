# src/qtrader/providers/massive/realtime/websocket.py

from massive import WebSocketClient

class MassiveWebSocket:
    """
    Minimal wrapper around Massive's WebSocketClient.
    """

    def __init__(self, api_key: str):
        self.ws = WebSocketClient(api_key=api_key)

    def subscribe(self, channels):
        """
        Subscribe to one or more channels.
        channels: list of strings, e.g. ['trades:AAPL', 'quotes:MSFT']
        """
        self.ws.subscribe(channels)

    def run(self, on_message):
        """
        Run the websocket and call on_message callback for each message.
        on_message: function that takes a single argument (the event dict)
        """
        self.ws.run(on_message)
