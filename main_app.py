import tkinter as tk
from tkinter import ttk
from dashboard.dashboard_panel import DashboardPanel

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
        control_frame = tk.Frame(root, padx=10, bg="#1E1E1E")
        control_frame.pack(side="left", fill="y")

        # Right panel
        self.right_panel = DashboardPanel(root)
        self.right_panel.pack(side="right", fill="y")


        # Overlay Button Style
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Overlay.TButton",
            font=("Segoe UI", 8, "bold"),
            foreground="#AAAAAA",
            background="#000000",
            padding=(8, 6),
            borderwidth=0,
            relief="flat"
        )
        
        style.configure(
            "OverlayActive.TButton",
            font=("Segoe UI", 9, "bold"),
            foreground="#00FF88",
            background="#000000",
        )
        
        style.map(
            "Overlay.TButton",
            background=[("active", "#111111")]
        )
        
        # Scrollable Overlay Container 
        self.overlay_container = tk.Frame(self.center_panel, bg="#000000")
        self.overlay_container.place(x=12, y=12, relwidth=0.95)
        style.configure(
            "Dark.Horizontal.TScrollbar",
            troughcolor="#1A1A1A",
            background="#1A1A1A",
            darkcolor="#1A1A1A",
            lightcolor="#1A1A1A",
            bordercolor="#1A1A1A",
            arrowcolor="#000000"
        )
        self.overlay_canvas = tk.Canvas(
            self.overlay_container,
            bg="#000000",
            height=40,
            highlightthickness=0
        )
        self.overlay_canvas.pack(side="top", fill="x", expand=True)

        overlay_scroll = ttk.Scrollbar(
            self.overlay_container,
            orient="horizontal",
            command=self.overlay_canvas.xview,
            style="Dark.Horizontal.TScrollbar"
        )
        overlay_scroll.pack(side="bottom", fill="x")

        self.overlay_canvas.configure(xscrollcommand=overlay_scroll.set)

        # Inner frame 
        self.overlay_panel = tk.Frame(self.overlay_canvas, bg="#000000")
        self.overlay_canvas.create_window(
            (0, 0),
            window=self.overlay_panel,
            anchor="nw"
        )

        # Update scroll region
        self.overlay_panel.bind(
            "<Configure>",
            lambda e: self.overlay_canvas.configure(
                scrollregion=self.overlay_canvas.bbox("all")
            )
        )


        self.overlay_buttons = {}
        
        crypto_list = [
            ("solusdt",  "SOL/USDT",  ),
            ("btcusdt",  "BTC/USDT",  ),
            ("ethusdt",  "ETH/USDT",  ),
            ("bnbusdt",  "BNB/USDT",  ),
            ("adausdt",  "ADA/USDT",  ),
            ("xrpusdt",  "XRP/USDT",  ),
            ("dogeusdt", "DOGE/USDT", ),
            ("dotusdt",  "DOT/USDT",  ),
            ("linkusdt", "LINK/USDT", ),
            ("ltcusdt",  "LTC/USDT",  ),
            ("shibusdt", "SHIB/USDT", )
        ]

        for symbol, display_name in crypto_list:
            btn = ttk.Button(
                self.overlay_panel,
                text=display_name,
                style="Overlay.TButton",
                command=lambda s=symbol: self.toggle_ticker(s)
            )
            btn.pack(side="left", padx=6)

            self.overlay_buttons[symbol] = btn

        # Add tickers
        self.add_ticker(self.left_panel, BTCTicker )
        self.add_ticker(self.left_panel, ETHTicker )
        self.add_ticker(self.left_panel, BNBTicker )
        self.add_ticker(self.left_panel, SOLTicker )
        self.add_ticker(self.left_panel, ADATicker )
        self.add_ticker(self.left_panel, XRPTicker )
        self.add_ticker(self.left_panel, DOGETicker)
        self.add_ticker(self.left_panel, DOTTicker )
        self.add_ticker(self.left_panel, LINKTicker)
        self.add_ticker(self.left_panel, LTCTicker )
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
        if hasattr(self, "active_chart"):
            self.active_feed.stop()
            self.active_chart.pack_forget()

        # reset all labels
        for btn in self.overlay_buttons.values():
            btn.configure(style="Overlay.TButton")

        # highlight active
        self.overlay_buttons[symbol].configure(
            style="OverlayActive.TButton"
        )

        self.active_chart = CandleChart(self.center_panel, title=symbol.upper())
        self.active_chart.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.active_feed = BinanceKlineFeed(
            chart=self.active_chart,
            root=self.root,
            symbol=symbol,
            interval="5m"
        )
        self.active_feed.start()
        self.overlay_panel.lift()
        self.overlay_container.lift()


    def add_ticker(self, parent, TickerClass):
        ticker = TickerClass(parent)   # Create ticker object
        ticker.pack(fill="x", pady=6, padx=6)

        self.style_ticker(ticker.frame)  # Style

        ticker.start()
        self.tickers.append(ticker)


    def on_closing(self):
            if hasattr(self, "active_feed"):
                try:
                    self.active_feed.stop()
                    print("Active feed stopped.")
                except Exception as e:
                    print(f"Error stopping active feed: {e}")
    
            self.root.after(100, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTickerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
