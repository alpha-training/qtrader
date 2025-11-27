# src/qtrader/providers/massive/historical/ingest.py

from ..normalize import normalize_snapshot, normalize_trade, normalize_aggregate
import logging

logger = logging.getLogger(__name__)


class MassiveHistoricalIngestor:
    """
    Push historical data into qtrader using normalization.
    """

    def __init__(self, storage_handler):
        """
        :param storage_handler: object that knows how to write normalized data into qtrader
        """
        self.storage = storage_handler

    def ingest_snapshots(self, snapshots: dict):
        for symbol, data in snapshots.items():
            try:
                norm_data = normalize_snapshot(data)
                self.storage.write_snapshot(symbol, norm_data)
            except Exception as e:
                logger.exception("Error ingesting snapshot for %s: %s", symbol, e)

    def ingest_trades(self, trades: dict):
        for symbol, data in trades.items():
            try:
                norm_data = [normalize_trade(d) for d in data]
                self.storage.write_trades(symbol, norm_data)
            except Exception as e:
                logger.exception("Error ingesting trades for %s: %s", symbol, e)

    def ingest_aggregates(self, aggregates: dict):
        for symbol, data in aggregates.items():
            try:
                norm_data = [normalize_aggregate(d) for d in data]
                self.storage.write_aggregates(symbol, norm_data)
            except Exception as e:
                logger.exception("Error ingesting aggregates for %s: %s", symbol, e)
