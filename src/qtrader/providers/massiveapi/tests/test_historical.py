# src/qtrader/providers/massive/tests/test_historical.py

import pytest
from qtrader.providers.massiveapi.historical.rest import MassiveREST
from qtrader.providers.massiveapi.historical.ingest import HistoricalIngest
from qtrader.providers.massiveapi.historical.downloader import HistoricalDownloader

API_KEY = "rSQLz8C1muscWBydEkoAWpW4RH9CW_wq"

def test_download_and_ingest():
    client = MassiveREST(API_KEY)
    raw = client.fetch_aggs("AAPL", from_="2023-06-01", to="2023-06-02", limit=2)
    
    assert len(raw) > 0, "No raw data returned"

    ingest = HistoricalIngest()
    normalized = ingest.ingest(raw)

    assert all("datetime" in row for row in normalized)
    assert all("open" in row for row in normalized)
    assert all("close" in row for row in normalized)
