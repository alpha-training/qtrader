# src/qtrader/providers/massive/normalize.py

from massive.websocket.models import WebSocketMessage
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# -------------------------------
# Real-time normalization
# -------------------------------

def normalize_message(msg: WebSocketMessage) -> Dict[str, Any]:
    """
    Normalize a single WebSocket message to a standard schema.
    """
    try:
        # Example: convert fields from Massive to qtrader expected fields
        return {
            "symbol": msg.symbol,
            "timestamp": msg.timestamp,
            "price": msg.price,
            "size": getattr(msg, "size", None),
            "type": msg.type,
            "raw": msg.json(),  # keep original JSON for debugging if needed
        }
    except Exception as e:
        logger.exception("Failed to normalize WebSocket message: %s", e)
        return {}

# -------------------------------
# Historical normalization
# -------------------------------

def normalize_snapshot(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize snapshot data (REST) for qtrader.
    """
    try:
        return {
            "symbol": data.get("symbol"),
            "bid": data.get("bid"),
            "ask": data.get("ask"),
            "last_price": data.get("last"),
            "volume": data.get("volume"),
            "timestamp": data.get("timestamp"),
            "raw": data,
        }
    except Exception as e:
        logger.exception("Failed to normalize snapshot: %s", e)
        return {}

def normalize_trade(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a single trade record.
    """
    try:
        return {
            "symbol": data.get("symbol"),
            "price": data.get("price"),
            "size": data.get("size"),
            "timestamp": data.get("timestamp"),
            "exchange": data.get("exchange"),
            "raw": data,
        }
    except Exception as e:
        logger.exception("Failed to normalize trade: %s", e)
        return {}

def normalize_aggregate(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize OHLCV aggregate data.
    """
    try:
        return {
            "symbol": data.get("symbol"),
            "open": data.get("open"),
            "high": data.get("high"),
            "low": data.get("low"),
            "close": data.get("close"),
            "volume": data.get("volume"),
            "timestamp": data.get("timestamp"),
            "interval": data.get("interval"),
            "raw": data,
        }
    except Exception as e:
        logger.exception("Failed to normalize aggregate: %s", e)
        return {}
