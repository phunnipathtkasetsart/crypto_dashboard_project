import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading
from Tickers.btc_ticker import BTCTicker
from Tickers.eth_ticker import ETHTicker

class MultiTickerApp:
    def __init__(self, root):
        self.root = root
        root.title("Crypto Dashboard")
        root.geometry("800x300")

        self.tickers = []    # Store ticker objects

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Add tickers here
        self.add_ticker(frame, BTCTicker)
        self.add_ticker(frame, ETHTicker)

    def add_ticker(self, parent, TickerClass):
        ticker = TickerClass(parent)
        ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        ticker.start()
        self.tickers.append(ticker)

    def on_closing(self):
        for t in self.tickers:
            t.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTickerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
