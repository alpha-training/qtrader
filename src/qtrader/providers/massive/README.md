# Massive.com Adapter for qtrader

This repository handles the connection between the **Massive.com** market data API and our **kdb+** system. It handles both real-time streaming data and historical data downloads.

---

## Quick Start (How to Run)

If you just want to get the data flowing, follow these steps.

### 1. Prerequisites
Ensure you have the following installed in your VS Code environment:
* **kdb+ (q)** (with `embedPy` installed)
* **Python 3.x**
* The Massive Python client:
    ```bash
    pip install massive-client
    ```

### 2. Configuration
Before running, ensure your API Key is set.
Open `src/qtrader/providers/massive/realtime/stream.py` and check the client setup:
```python
client = WebSocketClient(
    api_key="YOUR_API_KEY_HERE",  # Ensure this is correct
    feed=Feed.Delayed,
    market=Market.Stocks
)
```
### 3. Running the Real-Time Feed
We do not run the Python script directly. We run the **Q Feedhandler**, which automatically loads the Python stream in the background.

1. Open the **Terminal** in VS Code (`Ctrl + \``).
2. Navigate to the realtime directory:
   ```bash
   cd src/qtrader/providers/massive/realtime
   ```
3. Run the Q script:
   ```bash
   q feed.q
   ```

**What happens next?**
* The system connects to Massive.com.
* You will see "Feedhandler Running..." in the console.
* Every 1 second, a list of quotes (Time, Sym, Open, High, Low, Close) will be printed to the console (or sent to the tickerplant).

---

## 📂 Directory Structure

Here is where everything lives. The most important files for the real-time feed are in the `realtime/` folder.

```text
src/qtrader/providers/massive/
│
├── __init__.py               <-- Makes this folder a Python package
│
├── realtime/                 <-- CURRENT FOCUS
│   ├── __init__.py
│   ├── feed.q                <-- The ENTRY POINT. Run this file.
│   ├── stream.py             <-- Python logic (API connection & Buffer)
│   └── websocket.py          <-- Lower level websocket logic (optional)
│
├── historical/               <-- For backfilling data
│   ├── __init__.py
│   ├── rest.py               <-- REST API wrapper
│   ├── downloader.py         <-- Bulk downloads / batch jobs
│   └── ingest.py             <-- Pushes historical data into q
│
├── normalize.py              <-- Converts provider JSON → q-friendly schema
├── utils.py                  <-- Retry logic, rate-limit, helpers
│
└── tests/
    ├── test_realtime.py
    └── test_historical.py
```

### What is `__init__.py`?
You will see this file in every folder. It tells Python to treat that directory as a **package**, allowing us to import files from one folder to another. It is often empty, which is normal.

---

## Developer Notes

### How it works (The Architecture)
We use **embedPy** to bridge Python and Q.
1. **Python (`stream.py`)**: Connects to the websocket in a background thread and collects data into a buffer.
2. **Q (`feed.q`)**: Runs a timer every 1 second. It tells Python to "drain" that buffer, then flips the data into kdb+ lists and processes it.

### Adding new subscriptions
To subscribe to more tickers, edit `stream.py`:
```python
# Subscribe to all stocks
client.subscribe("A.*")

# OR Subscribe to specific tickers
# client.subscribe("A.AAPL", "A.MSFT")
```

### Reference Documentation
* **Official Massive Python Docs:** [https://github.com/massive-com/client-python](https://github.com/massive-com/client-python)