# Market Data Analyzer

A Python tool for analyzing financial market datasets.  
This project demonstrates **data analysis, visualization, and financial modeling** using Python.

---

## Features

- Load CSV market data or fetch real-time stock data via Yahoo Finance
- Perform basic statistical analysis (average, max, min, volume)
- Calculate daily returns
- Calculate **moving averages** (7-day & 30-day)
- Measure **volatility** of stocks
- Visualize:
  - Price trends
  - Trading volume
  - Moving averages
  - Candlestick charts
  - Multi-stock correlation heatmaps
- Multi-stock portfolio simulation

---

## Technologies

- Python
- pandas
- matplotlib
- seaborn
- yfinance
- mplfinance

---

## Project Structure

```text
market-data-analyzer
│
├── data
│   └── sample_stock_data.csv
│
├── src
│   ├── fetch_data.py
│   ├── load_data.py
│   ├── analyze_data.py
│   ├── visualize_data.py
│   ├── portfolio_analysis.py
│   └── main.py
│
├── requirements.txt
└── README.md

git clone https://github.com/Lamie14/market-data-analyzer.git
cd market-data-analyzer
pip install -r requirements.txt
python src/main.py,

Fetching data for AAPL...

Market Statistics
-----------------
average_close_price: 182.34
max_close_price: 197.90
min_close_price: 162.12
average_volume: 54321000

Market Volatility
-----------------
0.021

Portfolio simulation completed
