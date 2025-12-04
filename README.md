# qtrader

**qtrader** is a free-to-use backtesting and trading platform built in Python and kdb+.

## What is kdb+?
kdb+ is a high-performance time-series database paired with its own vector programming language, q. It is ubiquitous across financial markets — used by all of the world’s top investment banks and by leading quantitative trading firms such as **Citadel**, **Millennium**, **Virtu**, **Squarepoint**, and others. In the crypto space, **BitMEX** has long been a prominent user of kdb+, and newer institutional players such as **B2C2** also rely on it for real-time analytics and trading infrastructure.

## Why should I use it?
For most of its history, kdb+ was paid-only — and expensive — putting it out of reach for independent traders. However in November 2025, the owners of kdb+, [KX Systems](https://kx.com), announced that its new Community Edition would **now be free for commercial use**. This means that, for the first time ever, independent quants can run kdb+ commercially without a licence fee.

## What is qtrader?
If kdb+ is the world's fastest Formula 1 engine, qtrader is the car built around it — assembled from the following components:

1. A kdb+ package manager and suite of modules called **qi**
2. Python wrappers and a **Python bridge** for live and historical data
3. A suite of YAML **process templates** and recipes
4. A Python-esque **domain-specific language** for backtesting called **qsharpe**, which translates into q
5. A suite of algo containers and execution engines
6. Interfaces with low- or no-cost data providers such as **Yahoo Finance** and **Massive** (formerly Polygon.io)
7. Interfaces with execution gateways including **Interactive Brokers**, **Alpaca**, **Binance**, **Kraken**, and **Deribit**
8. Lightweight web user interfaces

**qtrader** is owned and maintained by kdb+ engineering firm [AlphaKDB](https://alphakdb.com). Its modular architecture means that different configurations of *“car”* are not only permitted, but positively encouraged.

## Processes
A snapshot of the processes contained in **qtrader** may be found by copying and pasting the below into the [process editor](https://mermaid.live/edit):

```
flowchart TB
    providers("providers") --> tp1["tp1"]
    tp1 --> ctp("ctp") & eng["engines 1-n"]
    ctp --> rdb["rdb"] & lvc("lvc1") & wdb["wdb"]
    tp1 -.-> tp1log["log1"]
    eng --> net("net") & tp2["tp2"]
    net --> om("om") & tp2
    om --> broker["broker"] & tp2
    wdb -- 15m --> disk["Disk"]
    disk -. Mapped .-> hdb("hdb")
    tp2 --> ctp
    tp2 -.-> tp2log["log2"]
    hdb <--> gw["gw"]
    rdb <--> gw
    api("api")
    c2("c2")
    ui("ui")

    eng@{ shape: processes}
    providers@{ shape: processes}
    broker@{ shape: processes}
    tp1log@{ shape: lin-cyl}
    tp2log@{ shape: lin-cyl}
    disk@{ shape: lin-cyl}
```

## Python users
Python users can analyse historical and live data, subscribe to event streams, and export backtest results — while strategy logic and order routing run in kdb+ for speed and safety.

## How do I use qtrader?

```bash
git clone https://github.com/alphakdb/repos/qtrader
cd qtrader
pip install -e .
qtrader up equities.us1
```
For the full guide, see [docs/quickstart.md](docs/quickstart.md).

## Design principles
We tried to abide by various [design principles](docs/design_principles.md) when building the tool. It is up to others to judge how well we adhered to them.

## Helper videos
On AlphaKDB’s YouTube channel, **kdb+ starting grid**, you’ll find a series of short videos showing exactly what you need to do to trade with kdb+, whether with paper money or real capital. The video **“Trading with kdb+ in under 10 minutes”** is a good place to start.

## License
**qtrader** is free to use when running on the kdb+ Community Edition. Users running the commercial edition of kdb+ may require a licence — please [contact us](mailto:sales@alphakdb.com) for details.

## Feedback and suggestions
We welcome feedback at [qtrader@alphakdb.com](mailto:qtrader@alphakdb.com). By submitting feedback, feature requests, or ideas related to this project through any channel, you agree to the terms in [FEEDBACK-LICENSE.txt](https://raw.githubusercontent.com/alpha-training/qi/refs/heads/main/FEEDBACK-LICENSE.txt). Active users can also join the community Slack (link in repo) for help, discussions, and strategy sharing.
