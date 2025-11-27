# src/qtrader/providers/massive/realtime/stream.py

import logging
from queue import Queue, Empty
from threading import Thread, Event
from typing import Callable, Optional, Dict, Any

logger = logging.getLogger(__name__)


class RealTimeStreamHandler:
    """
    Handles streaming messages from MassiveRealtimeClient.
    Queues them and provides a background consumer that pushes messages
    into a downstream consumer function (e.g., your trading engine).
    """

    def __init__(self, max_queue_size: int = 10000):
        self._queue: Queue[Dict[str, Any]] = Queue(maxsize=max_queue_size)
        self._stop_event: Event = Event()
        self._thread: Optional[Thread] = None

    def handle(self, msg: Dict[str, Any]) -> None:
        """
        Called by websocket client for each normalized message.
        Adds the message to the internal queue.
        """
        try:
            self._queue.put_nowait(msg)
        except Exception:
            logger.warning("Queue full, dropping message: %s", msg)

    def start_consuming(
        self,
        consumer_func: Callable[[Dict[str, Any]], None],
        poll_interval: float = 0.01,
    ) -> None:
        """
        Start a background thread that reads messages from the queue
        and calls `consumer_func(msg)` for each.
        """

        if self._thread and self._thread.is_alive():
            logger.warning("Stream consumer already running")
            return

        self._stop_event.clear()

        def _consume_loop() -> None:
            while not self._stop_event.is_set():
                try:
                    msg = self._queue.get(timeout=poll_interval)
                    consumer_func(msg)
                except Empty:
                    continue
                except Exception as e:
                    logger.exception("Error consuming message: %s", e)

        self._thread = Thread(target=_consume_loop, daemon=True)
        self._thread.start()
        logger.info("RealTimeStreamHandler consumer started")

    def stop_consuming(self) -> None:
        """
        Stop the background consumer thread gracefully.
        """
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("RealTimeStreamHandler consumer stopped")

    def clear_queue(self) -> None:
        """
        Optional helper to clear all queued messages.
        """
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except Empty:
                break
