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