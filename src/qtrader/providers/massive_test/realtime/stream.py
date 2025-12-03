# src/qtrader/providers/massiveapi/realtime/stream.py

from massive import WebSocketClient
from massive.websocket.models import EquityAgg, Feed, Market
from typing import List, Callable
import pandas as pd
from ..normalize import normalize_aggs

class EquityStream:
    def __init__(self, api_key: str, feed=Feed.Delayed, market=Market.Stocks):
        self.client = WebSocketClient(api_key=api_key, feed=feed, market=market)
        self.callbacks: List[Callable[[pd.DataFrame], None]] = []
        self.buffer: List[EquityAgg] = []

    def subscribe(self, *tickers):
        """Subscribe to one or more tickers."""
        for t in tickers:
            self.client.subscribe(t)

    def on_message(self, callback: Callable[[pd.DataFrame], None]):
        """
        Register a callback function that will receive normalized DataFrame rows.
        """
        self.callbacks.append(callback)

    def _handle_msg(self, msgs: List[EquityAgg]):
        """
        Internal handler: normalize messages and call registered callbacks.
        """
        self.buffer.extend(msgs)

        # Convert to DataFrame and pass to callbacks
        for m in msgs:
            df = normalize_aggs([m], ticker=m.symbol)
            for cb in self.callbacks:
                cb(df)

    def run(self):
        """Start streaming. Blocks until Ctrl+C."""
        self.client.run(self._handle_msg)
