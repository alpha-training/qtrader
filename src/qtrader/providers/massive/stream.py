from massive import WebSocketClient
from massive.websocket.models import WebSocketMessage
from typing import List

# 1. SETUP
API_KEY = "rSQLz8C1muscWBydEkoAWpW4RH9CW_wq"
# We will force this URL manually below
DELAYED_URL = "wss://delayed.polygon.io/stocks" 

SUBSCRIPTIONS = ["Q.AAPL", "T.AAPL"]

def handle_msg(msgs: List[WebSocketMessage]):
    for m in msgs:
        if m.event_type == "Q":
            print(f"QUOTE | {m.symbol} | Bid: ${m.bid_price} x {m.bid_size}")
        elif m.event_type == "T":
            print(f"TRADE | {m.symbol} | ${m.price}")

if __name__ == "__main__":
    print("--- 1. INITIALIZING CLIENT ---")
    ws = WebSocketClient(
        api_key=API_KEY, 
        subscriptions=SUBSCRIPTIONS,
        verbose=True
    )
    
    # --- THE FIX ---
    # We manually overwrite the URL to point to the Delayed Cluster
    print(f"--- 2. OVERRIDING URL TO: {DELAYED_URL} ---")
    ws.url = DELAYED_URL 
    
    print("--- 3. CONNECTING ---")
    ws.run(handle_msg=handle_msg)