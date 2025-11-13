# qtrader quickstart

This guide takes you from installation → configuration → backtesting → paper trading → live trading, including installation of the optional [qtrader-ui](https://github.com/alpha-training/qtrader-ui) web interface.

## 1. Clone the repository

```bash
git clone https://github.com/alphakdb/repos/qtrader
cd qtrader
```

## 2. Create and activate a Python environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

## 3. Install qtrader

```bash
pip install -e .
```

or:

```bash
pip install -r requirements.txt
```

This installs:

- the **qtrader CLI** (`qtrader`)
- Python wrappers & data interfaces  
- the Python ↔ kdb+ bridge  
- backtesting and live trading utilities  

## 4. Install kdb+ Community Edition

Download:

Visist [kx.com](https://kx.com) and obtain the community edition.

Add `q` to your PATH, then verify:

```bash
q
```

You should see the kdb+ banner and a `q)` prompt.

## 5. Initialise your qtrader environment

```bash
qtrader init
```

This creates the project structure:

- `config/` — data providers, execution gateways  
- `accounts/` — paper & live accounts  
- `strategies/` — your strategy templates  
- `logs/`  
- `data/` (optional)  

## 6. Verify your installation

```bash
qtrader check
```

This confirms:

- Python ↔ kdb+ connectivity  
- qi availability  
- data-provider connectivity  
- process templates  
- environment variables  

## 7. Run your first backtest

```bash
qtrader backtest strategies/example.yaml
```

This will:

- load a qsharpe strategy  
- fetch data (Yahoo/Massive)  
- translate to q  
- run the backtest inside kdb+  
- output results to `backtests/` (plots, CSV, metrics)  

## 8. Start trading (paper or live)

### Paper trading

```bash
qtrader trade --account paper
```

Paper accounts require **no API keys**.

### Live trading

Configure your preferred gateway in:

```
config/accounts/<gateway-name>.yaml
```

Supported gateways include:

- **Interactive Brokers**
- **Alpaca**
- **Binance**
- **Kraken**
- **Deribit**

Then:

```bash
qtrader trade --account live-ibkr
```

Or:

```bash
qtrader trade --account live-binance
```

## 9. Install the optional qtrader-ui (Web Interface)

The UI provides dashboards for:

- live positions  
- market data streams  
- portfolio analytics  
- backtest reports  
- account monitoring  

### Install qtrader-ui

```bash
git clone https://github.com/alpha-training/qtrader-ui
cd qtrader-ui
npm install
npm run build   # or: npm run dev
```

To run the UI:

```bash
npm run start
```

Or with dev mode:

```bash
npm run dev
```

The UI will attempt to connect to your running qtrader services automatically (configurable in `.env`).

## 10. You're good to go

You now have:

- kdb+ + q running locally  
- the qtrader CLI  
- strategy templates  
- data and execution gateways  
- optional web UI  

You can begin defining strategies in:

```
strategies/
```

And trading with:

```
qtrader trade --account paper
```

For questions, join the **AlphaKDB** community Slack (TBD).
