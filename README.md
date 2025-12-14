# Crypto Dashboard

A professional, real-time cryptocurrency monitoring suite built with **Python** and **Tkinter**. This application provides a unified interface to track live prices, analyze market trends with interactive candlestick charts, and stay updated with global crypto news.



---

## Key Features

* **Real-time Price Tickers**: High-frequency price updates for major assets (BTC, ETH, SOL, etc.) using **Binance WebSockets**.
* **Interactive Candlestick Charts**: Integrated **mplfinance** charts that update live as new "kline" data arrives.
* **Market Intelligence**: 
    * **Global Stats**: Track BTC dominance and total market cap via **CoinGecko**.
    * **Top Movers**: Real-time list of the top 5 gainers and losers in the last 24 hours.
* **Live News Feed**: A curated stream of the latest market-moving headlines via the **CryptoPanic API**.
* **Sleek Dark UI**: Custom-styled dark theme optimized for readability, featuring a scrollable sidebar and responsive layout.

---

## Technical Stack

| Component | Technology |
| :--- | :--- |
| **GUI Framework** | Python Tkinter (with Custom TTK Styling) |
| **Data Viz** | Matplotlib, mplfinance |
| **Data Processing** | Pandas, JSON |
| **Networking** | Websockets (Real-time), Requests (REST) |
| **Data Sources** | Binance API, CoinGecko API, CryptoPanic API |

---

## Project Architecture

The project is modularized for easy maintenance and scalability:

* **`main_app.py`**: The central controller. Handles the main window, UI theme, and initializes the ticker/chart components.
* **`crypto_ticker.py`**: A robust base class for individual asset cards. It manages its own dedicated WebSocket connection.
* **`tickers/ticker_all.py`**: Contains specialized classes for various trading pairs (BTC, ETH, XRP, etc.).
* **`charts/`**:
    * `chart.py`: Handles the rendering of the candlestick plot using Matplotlib.
    * `realtime.py`: Logic for fetching historical data and managing the live Binance kline stream.
* **`dashboard/`**:
    * `dashboard_panel.py`: Controls the right-hand panel (Market Overview & News).
    * `market_api.py`: Standardizes requests to CoinGecko and CryptoPanic.
* **`test_api.py`**: A standalone diagnostic utility to verify API and WebSocket health.

---
## Known bugs
- News API is not working
- The left panel price tickers are not responsive

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- A stable internet connection
- Install Dependencies : pip install requests pandas matplotlib mplfinance websocket-client

### 1. Clone the Project
```bash
git clone [https://github.com/yourusername/crypto-dashboard.git](https://github.com/yourusername/crypto-dashboard.git)
cd crypto-dashboard
