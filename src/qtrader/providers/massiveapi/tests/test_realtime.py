# src/qtrader/providers/massive/tests/test_realtime.py

import pytest
from qtrader.providers.massiveapi.realtime.stream import MassiveStream

API_KEY = "rSQLz8C1muscWBydEkoAWpW4RH9CW_wq"

def test_realtime_subscribe():
    stream = MassiveStream(API_KEY)
    
    # Subscribe to a single ticker
    stream.subscribe_trades("AAPL")

    # Simple message counter
    received = []

    def callback(msg):
        received.append(msg)
        if len(received) >= 1:  # stop after first message
            raise SystemExit  # exits websocket cleanly for testing

    try:
        stream.start(callback)
    except SystemExit:
        pass

    assert len(received) >= 1
    assert "ticker" in received[0] or "sym" in received[0]
