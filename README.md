# 📈 Market Data Analyzer

A Python-based financial market analysis tool that fetches real-time stock data, performs statistical and portfolio analysis, and generates professional visualisations — all from the command line.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![pandas](https://img.shields.io/badge/pandas-2.x-150458?logo=pandas)
![matplotlib](https://img.shields.io/badge/matplotlib-3.x-11557c)
![yfinance](https://img.shields.io/badge/yfinance-0.2-green)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

---

## 📸 Sample Output

> *(Add screenshots of your charts here once generated)*

```
Fetching data for AAPL...

Market Statistics
-----------------
average_close_price : 182.34
max_close_price     : 197.90
min_close_price     : 162.12
average_volume      : 54,321,000

Market Volatility
-----------------
Annualised Volatility: 33.26%

Portfolio Simulation
--------------------
Initial Investment : $10,000.00
Final Value        : $12,847.32
Total Return       : +28.47%
Portfolio simulation completed ✅
```

---

## ✨ Features

- 📥 **Dual data loading** — fetch live data via Yahoo Finance or load from a local CSV
- 📊 **Statistical analysis** — average, max, min price and volume summaries
- 📉 **Daily returns** — percentage change calculations per trading day
- 📈 **Moving averages** — 7-day and 30-day MA overlaid on price charts
- 🔥 **Volatility measurement** — annualised standard deviation of returns
- 🕯️ **Candlestick charts** — OHLC visualisation using mplfinance
- 🌡️ **Correlation heatmaps** — multi-stock relationship analysis with seaborn
- 💼 **Portfolio simulation** — simulate returns across multiple stocks

---

## 📁 Project Structure

```
market-data-analyzer/
├── data/
│   └── sample_stock_data.csv       # Sample OHLCV dataset for offline use
├── src/
│   ├── fetch_data.py               # Fetch live data from Yahoo Finance
│   ├── load_data.py                # Load and validate CSV data
│   ├── analyze_data.py             # Statistical analysis & returns
│   ├── visualize_data.py           # All chart generation
│   ├── portfolio_analysis.py       # Multi-stock portfolio simulation
│   └── main.py                     # CLI entry point
├── outputs/                        # Generated charts saved here (git-ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/Lami14/market-data-analyzer.git
cd market-data-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the analyser
```bash
# Fetch live data for a stock
python src/main.py --ticker AAPL --period 6mo

# Use local CSV data
python src/main.py --file data/sample_stock_data.csv

# Analyse multiple stocks
python src/main.py --tickers AAPL MSFT GOOGL --period 1y

# Run portfolio simulation
python src/main.py --portfolio AAPL MSFT TSLA --investment 10000
```

---

## 📊 Visualisations

| Chart | Description |
|---|---|
| Price Trend | Closing price over time with moving averages |
| Volume Chart | Daily trading volume bar chart |
| Candlestick | OHLC candlestick chart via mplfinance |
| Correlation Heatmap | Pearson correlation between multiple stocks |
| Portfolio Growth | Simulated portfolio value over time |

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, transformation |
| `yfinance` | Live stock data from Yahoo Finance |
| `matplotlib` | Price, volume and moving average charts |
| `seaborn` | Correlation heatmaps |
| `mplfinance` | Candlestick OHLC charts |

---

## 💡 What I Learned

- Working with real financial time-series data using pandas
- Fetching and processing live market data with the yfinance API
- Calculating financial metrics: daily returns, moving averages, annualised volatility
- Building multi-panel visualisations with matplotlib and seaborn
- Structuring a modular Python project with clean separation of concerns

---

## 🔮 Future Improvements

- [ ] Add Bollinger Bands and RSI indicators
- [ ] Export analysis report to PDF
- [ ] Add a Streamlit dashboard for interactive exploration
- [ ] Write unit tests with `pytest`
- [ ] Add CLI argument validation and error handling

---

## 📄 License

MIT License — feel free to fork and build on this project.

---

*Built by [Lamla](https://github.com/Lami14) · Financial Data Analysis Portfolio Project*

