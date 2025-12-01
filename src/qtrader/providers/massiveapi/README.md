# qtrader massive.com adaptor

* Start by looking at [https://github.com/massive-com/client-python](https://github.com/massive-com/client-python)
* Only include the minimal amount of code we need

## Directory structure


	(under src/qtrader/providers/massive)
	
    __init__.py

    # Real-time ingestion
    realtime/
        __init__.py
        websocket.py    ← realtime ticks/quotes/bars
        stream.py       ← API wrappers, reconnect logic

    # Historical ingestion
    historical/
        __init__.py
        rest.py         ← REST API wrapper
        downloader.py   ← bulk downloads / batch jobs
        ingest.py       ← push historical data into q

    # Shared logic
    normalize.py        ← converts provider JSON → q-friendly schema
    utils.py            ← retry logic, rate-limit, helpers

    # Tests
    tests/
        test_realtime.py
        test_historical.py

    README.md
