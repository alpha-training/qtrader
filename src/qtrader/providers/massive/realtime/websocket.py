# src/qtrader/providers/massive/realtime/websocket.py

from massive.websocket import WebSocketClient
from massive.websocket.models.models import WebSocketMessage
import threading
import logging
from typing import Optional

from ..normalize import normalize_message  # you’ll write this
from ..stream import RealTimeStreamHandler  # you’ll define this in stream.py
from ..utils import retry  # maybe for reconnect logic / backoff

logger = logging.getLogger(__name__)


class MassiveRealtimeClient:
    def __init__(self, api_key: str, subscriptions: list[str], stream_handler: RealTimeStreamHandler, **ws_kwargs):
        self.api_key = api_key
        self.subscriptions = subscriptions
        self.stream_handler = stream_handler
        self.ws_kwargs = ws_kwargs

        self._ws: Optional[WebSocketClient] = None
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def _on_message(self, msgs: list[WebSocketMessage]):
        for m in msgs:
            try:
                data = normalize_message(m)  # convert to standard schema
                self.stream_handler.handle(data)
            except Exception as e:
                logger.exception("Error processing message %s: %s", m, e)

    def _run_loop(self):
        self._ws = WebSocketClient(api_key=self.api_key,
                                   subscriptions=self.subscriptions,
                                   **self.ws_kwargs)
        self._ws.run(callback=self._on_message)  # <-- updated

    def start(self):
        if self._thread and self._thread.is_alive():
            logger.warning("Websocket already running")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("MassiveRealtimeClient started")

    def stop(self):
        self._stop_event.set()
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("MassiveRealtimeClient stopped")
