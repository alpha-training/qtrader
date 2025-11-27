# src/qtrader/providers/massive/tests/test_historical.py

import pytest
from unittest.mock import MagicMock
from ..historical.rest import MassiveRestClient  # you'll create this in rest.py
from ..normalize import normalize_snapshot, normalize_trade, normalize_aggregate

# -------------------------------
# Sample data fixtures
# -------------------------------

@pytest.fixture
def sample_snapshot():
    return {
        "symbol": "AAPL",
        "bid": 150.2,
        "ask": 150.3,
        "last": 150.25,
        "volume": 10000,
        "timestamp": 1700000000
    }

@pytest.fixture
def sample_trade():
    return {
        "symbol": "AAPL",
        "price": 150.25,
        "size": 10,
        "timestamp": 1700000000,
        "exchange": "NASDAQ"
    }

@pytest.fixture
def sample_aggregate():
    return {
        "symbol": "AAPL",
        "open": 149.0,
        "high": 151.0,
        "low": 148.5,
        "close": 150.25,
        "volume": 10000,
        "timestamp": 1700000000,
        "interval": "1m"
    }

# -------------------------------
# Tests
# -------------------------------

def test_normalize_snapshot(sample_snapshot):
    normalized = normalize_snapshot(sample_snapshot)
    assert normalized["symbol"] == "AAPL"
    assert normalized["bid"] == 150.2
    assert "raw" in normalized

def test_normalize_trade(sample_trade):
    normalized = normalize_trade(sample_trade)
    assert normalized["symbol"] == "AAPL"
    assert normalized["price"] == 150.25
    assert "raw" in normalized

def test_normalize_aggregate(sample_aggregate):
    normalized = normalize_aggregate(sample_aggregate)
    assert normalized["symbol"] == "AAPL"
    assert normalized["open"] == 149.0
    assert normalized["interval"] == "1m"
    assert "raw" in normalized
