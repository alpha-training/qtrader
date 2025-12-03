from massive import WebSocketClient
from massive.websocket.models import WebSocketMessage, Feed, Market
from typing import List

client = WebSocketClient(
    api_key="rSQLz8C1muscWBydEkoAWpW4RH9CW_wq",
    feed=Feed.Delayed,
    market=Market.Stocks
    )

# aggregates (per second)
client.subscribe("A.*") # single ticker
# client.subscribe("A.*") # all tickers
# client.subscribe("A.AAPL") # single ticker
# client.subscribe("A.AAPL", "AM.MSFT") # multiple tickers

def handle_msg(msgs: List[WebSocketMessage]):
    for m in msgs:
        print(m)

# print messages
client.run(handle_msg)