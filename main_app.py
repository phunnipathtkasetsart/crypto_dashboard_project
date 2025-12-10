import tkinter as tk
from tkinter import ttk

# Import all ticker files
from crypto_ticker import CryptoTicker
from tickers.ticker_all import BTCTicker
from tickers.ticker_all import ETHTicker
from tickers.ticker_all import BNBTicker
from tickers.ticker_all import SOLTicker
from tickers.ticker_all import ADATicker
from tickers.ticker_all import XRPTicker
from tickers.ticker_all  import DOGETicker
from tickers.ticker_all import DOTTicker
from tickers.ticker_all  import LINKTicker
from tickers.ticker_all import LTCTicker
from tickers.ticker_all  import SHIBTicker

# Import Chart
from charts.chart import CandleChart
from charts.realtime import BinanceKlineFeed

class MultiTickerApp:
    def __init__(self, root):
        self.root = root
        root.title("Crypto Dashboard")
        root.geometry("1200x600")
        self.tickers = []

        # Scrolls
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dark.Vertical.TScrollbar",
            troughcolor="#1A1A1A",
            background="#3A3A3A",
            darkcolor="#2E2E2E",
            lightcolor="#2E2E2E",
            bordercolor="#1A1A1A",
            arrowcolor="#5A5A5A"
        )
        
        left_container = tk.Frame(root, bg="#000000")
        left_container.pack(side="left", fill="y")
        self.canvas = tk.Canvas(left_container, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(side="left", fill="y")
        scrollbar = ttk.Scrollbar(
            left_container,
            orient="vertical",
            command=self.canvas.yview,
            style="Dark.Vertical.TScrollbar"
        )
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.left_panel = tk.Frame(self.canvas, bg="#1E1E1E")
        self.canvas.create_window((0, 0), window=self.left_panel, anchor="nw")
        self.left_panel.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.center_panel = tk.Frame(root, bg="#000000",width=150)
        self.center_panel.pack(side="left", fill="both", expand=True)


        # Control pannel
        control_frame = tk.Frame(root, padx=10,bg="#1E1E1E")
        control_frame.pack(side="left", fill="y")

        # Toggle Buttons
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Toggle.TButton",
            font=("Segoe UI", 11, "bold"),
            foreground="#FFFFFF",
            padding=10,
            borderwidth=0,
            focusthickness=0,
            relief="flat"
        )
        style.map(
            "Toggle.TButton",
            background=[
                ("active", "#3F3F3F"),   
                ("!active", "#333333")
            ],
        )
        

        # Dictionary storage
        self.tickers_dict = {}    # CryptoTicker object
        self.ticker_states = {}   # Boolean
        self.ticker_buttons = {}  # button object

        # List of cryptocurrencies
        crypto_list = [
            ("solusdt", "SOL/USDT"),
            ("btcusdt", "BTC/USDT"),
            ("ethusdt", "ETH/USDT"),
            ("bnbusdt", "BNB/USDT"),
            ("adausdt", "ADA/USDT"),
            ("xrpusdt", "XRP/USDT"),
            ("dogeusdt", "DOGE/USDT"),
        ]

        # Create everything automatically
        for symbol, display_name in crypto_list:
        
            # initial visibility
            self.ticker_states[symbol] = False

            # create ticker instance
            self.tickers_dict[symbol] = CryptoTicker(
                self.center_panel, symbol, display_name
            )

            # create button
            btn = ttk.Button(
                control_frame,
                text=f"Show {display_name}",
                style="Toggle.TButton",
                command=lambda s=symbol: self.toggle_ticker(s)
            )
            btn.pack(pady=5)

            # store button reference
            self.ticker_buttons[symbol] = btn

        # Add tickers
        self.add_ticker(self.left_panel, BTCTicker)
        self.add_ticker(self.left_panel, ETHTicker)
        self.add_ticker(self.left_panel, BNBTicker)
        self.add_ticker(self.left_panel, SOLTicker)
        self.add_ticker(self.left_panel, ADATicker)
        self.add_ticker(self.left_panel, XRPTicker)
        self.add_ticker(self.left_panel, DOGETicker)
        self.add_ticker(self.left_panel, DOTTicker)
        self.add_ticker(self.left_panel, LINKTicker)
        self.add_ticker(self.left_panel, LTCTicker)
        self.add_ticker(self.left_panel, SHIBTicker)


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


    def style_ticker(self, ticker_frame):
        ticker_frame.configure(bg="#000000")

        for widget in ticker_frame.winfo_children():
            try:
                widget.configure(bg="#000000", fg="#D0D0D0", font=("Segoe UI", 12))
            except:
                pass

        ticker_frame.configure(
            highlightbackground="#2A2A2A",
            highlightthickness=1,
            bd=0,
            padx=10,
            pady=10
        )

    def toggle_ticker(self, symbol):
            # Stop and remove the old chart/feed
            if hasattr(self, "active_chart"):
                self.active_feed.stop() 
                self.active_chart.pack_forget()

            # Create the new chart widget
            self.active_chart = CandleChart(self.center_panel, title=symbol.upper())
            self.active_chart.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
            self.active_feed = BinanceKlineFeed(
                chart=self.active_chart, 
                root=self.root,  
                symbol=symbol, 
                interval="5m"
            )
            self.active_feed.start()


    def add_ticker(self, parent, TickerClass):
        ticker = TickerClass(parent)   # Create ticker object
        ticker.pack(fill="x", pady=6, padx=6)

        self.style_ticker(ticker.frame)  # Style

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
