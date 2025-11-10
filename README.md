# qtrader

**qtrader** is a lightweight, free-to-use trading platform built on **kdb+**, with a built-in **python bridge**. If you’ve ever wanted the power of a hedge-fund-grade trading stack without the seven-figure licence costs, qtrader is for you.

## What is kdb+?
kdb+ is a high-performance time series database and programming language, q. It is ubiquitous in financial services, used by every one of the world's top ten investment banks, and leading trading shops such as **Citadel**, **Millennium**, **Virtu**, **Squarepoint** and others. In crypto, **BitMEX** has been a major user of kdb+ over the years, as are newer players such as **X**, **Y** and **Z** (TBD).

## Why should I use it?
Up until this year, kdb+ has been paid only, and expensive, putting it out of reach of independent traders. In November 2025, the owners of kdb+, [Kx Systems](https://kx.com), announced that its new community edition would **now be free for commercial use**. This means that, for the first time ever, independent quants can run kdb+ commercially without a licence fee.

## What is qtrader?
If we think of kdb+ as the world's fastest Formula 1 engine, **qtrader** is a car, built with the following components:

1. A kdb+ package manager and suite of modules called **qi**
2. A **python bridge** for live and historical data
3. A suite of yaml **process templates** and recipes
4. A **Domain Specific Language** for backtesting called **qsharpe**, which translates into q
5. A suite of algo containers and execution engines
6. Interfaces with low- or no-cost data providers such as **Yahoo Finance** and **Massive** (formerly Polygon.io)
7. Interfaces with execution gateways including **Interactive Brokers**, **Alpaca**, **Binance**, **Kraken**, and **Deribit**
8. Lightweight web user interfaces

**qtrader** is owned and maintained by kdb+ engineering firm [AlphaKDB](https://alphakdb.com). The modular fashion in which **qtrader** has been assembled means that different configurations of *"car"* are not only permitted, but positively encouraged.

## Python users
Python users can analyse historical and live data, subscribe to event streams, and export backtest results — but strategy logic and order routing run in kdb+ for speed and safety.

## How do I use qtrader?

	git clone https://github.com/alphakdb/repos/qtrader
	
## Helper videos
On AlphaKDB's YouTube channel, **kdb+ starting grid**, you'll find a series of short videos that explain exactly what you need to do to get trading with kdb+, whether that is just with funny money (paper trading) or real capital. The video **“Trading with kdb+ in under 10 minutes”** is a good place to start.

## License
**qtrader** is free-to-use when running on the kdb+ Community Edition. Users running the commercial edition of kdb+ may require a licence — please [contact us](mailto:sales@alphakdb.com) for details.

## Feedback and suggestions
We welcome feedback, which can be sent to [qtrader@alphakdb.com](mailto:qtrader@alphakdb.com). By submitting feedback, feature requests, or ideas related to this project, through any channel, you agree to the terms in [FEEDBACK-LICENSE.txt](https://raw.githubusercontent.com/alpha-training/qi/refs/heads/main/FEEDBACK-LICENSE.txt). Active users can also join the community Slack (link in repo) for help, discussions, and strategy sharing.





 
 




