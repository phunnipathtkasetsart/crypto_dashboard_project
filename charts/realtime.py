import websocket
import json
import threading
import pandas as pd
from datetime import datetime
import requests

class BinanceKlineFeed:
    def __init__(self, chart, root, symbol="btcusdt", interval="5m"):
        self.chart = chart
        self.root = root  # Store the Tkinter root window
        self.symbol = symbol
        self.interval = interval
        self.ws = None
        self.running = False
        
        # initial empty dataframe
        self.df = pd.DataFrame(
            columns=["Open", "High", "Low", "Close", "Volume"]
        )

    def _fetch_initial_data(self):
            """Fetches the last 100 historical klines using the Binance REST API."""
            url = "https://api.binance.com/api/v3/klines"
            params = {
                "symbol": self.symbol.upper(),
                "interval": self.interval,
                "limit": 60 # last 60 bars
            }

            try:
                response = requests.get(url, params=params)
                response.raise_for_status() # Raise an exception for bad status codes
                klines = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching initial data for {self.symbol}: {e}")
                return

            # historical data to DataFrame
            data = []
            for kline in klines:
                timestamp = datetime.fromtimestamp(kline[0] / 1000)
                data.append({
                    "Timestamp": timestamp,
                    "Open": float(kline[1]),
                    "High": float(kline[2]),
                    "Low": float(kline[3]),
                    "Close": float(kline[4]),
                    "Volume": float(kline[5]),
                })

            df = pd.DataFrame(data)
            if not df.empty:
                df = df.set_index("Timestamp")
                self.df = df 

                self.root.after(
                    0, 
                    lambda: self.chart.update_chart(self.df.tail(100))
                )

    def start(self):
        self.running = True
        threading.Thread(target=self._fetch_initial_data, daemon=True).start()
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False
        try:
            if self.ws:
                self.ws.close()
        except:
            pass

    def _run(self):
        url = (  f"wss://stream.binance.com:9443/ws/" f"{self.symbol}@kline_{self.interval}"   )
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_close=lambda ws: None
        )
        # Solution: Always use threading
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def _on_message(self, ws, message):
            # Debuggin code
            """print(f"Received: {message}") """ 
            """data = json.loads(message)"""

            data = json.loads(message)["k"]

            if not data["x"] and not self.df.empty and (data["t"] / 1000) == self.df.index[-1].timestamp():
                timestamp = self.df.index[-1]
            else:
                timestamp = datetime.fromtimestamp(data["t"] / 1000)


            # Update row 
            self.df.loc[timestamp] = [
                float(data["o"]),
                float(data["h"]),
                float(data["l"]),
                float(data["c"]),
                float(data["v"])
            ]

            df_tail = self.df.tail(60)

            self.root.after(
                0, 
                lambda: self.chart.update_chart(df_tail)
            )
