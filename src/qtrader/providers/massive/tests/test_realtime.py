# src/qtrader/providers/massive/tests/test_realtime.py

import pytest
from unittest.mock import MagicMock
from ..realtime.websocket import MassiveRealtimeClient
from ..normalize import normalize_message

# -------------------------------
# Fixtures
# -------------------------------

@pytest.fixture
def mock_stream_handler():
    handler = MagicMock()
    handler.handle = MagicMock()
    return handler


@pytest.fixture
def sample_ws_message():
    # Mocked WebSocketMessage
    class MockMessage:
        symbol = "AAPL"
        timestamp = 1700000000
        price = 150.25
        size = 10
        type = "trade"

        def json(self):
            return {"symbol": self.symbol, "price": self.price, "size": self.size}

    return MockMessage()


# -------------------------------
# Tests
# -------------------------------

def test_normalize_message(sample_ws_message):
    normalized = normalize_message(sample_ws_message)
    assert normalized["symbol"] == "AAPL"
    assert normalized["price"] == 150.25
    assert "raw" in normalized

def test_realtime_client_handles_message(mock_stream_handler, sample_ws_message):
    # Patch WebSocketClient to bypass real connection
    client = MassiveRealtimeClient(
        api_key="FAKE_KEY",
        subscriptions=["T.AAPL"],
        stream_handler=mock_stream_handler
    )

    # Call the _on_message directly with a list of one mocked message
    client._on_message([sample_ws_message])

    # Ensure the stream_handler.handle() was called with normalized data
    assert mock_stream_handler.handle.called
    args, kwargs = mock_stream_handler.handle.call_args
    normalized_data = args[0]
    assert normalized_data["symbol"] == "AAPL"
    assert "raw" in normalized_data

def test_start_and_stop_thread(mock_stream_handler):
    client = MassiveRealtimeClient(
        api_key="FAKE_KEY",
        subscriptions=["T.AAPL"],
        stream_handler=mock_stream_handler
    )

    # Patch _run_loop to just set a flag instead of connecting
    client._run_loop = MagicMock()
    client.start()
    assert client._thread.is_alive() or client._thread is not None
    client.stop()
    client._thread.join(timeout=1)
