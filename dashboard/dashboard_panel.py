
import tkinter as tk
import threading
from dashboard.market_api import (
    get_market_overview,
    get_top_movers,
    get_crypto_news
)

class DashboardPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0E0E0E", width=300)
        self.pack_propagate(False)

        self.build_ui()
        self.refresh_data()

    def section(self, title):
        outer = tk.Frame(self, bg="#121212")
        outer.pack(fill="x", padx=10, pady=8)
    
        tk.Label(
            outer,
            text=title,
            bg="#121212",
            fg="#AAAAAA",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=10, pady=(8, 4))
    
        body = tk.Frame(outer, bg="#121212")
        body.pack(fill="x", padx=10, pady=(0, 8))
    
        return body


    def build_ui(self):
        self.market_frame = self.section("Market Overview")
        self.gainers_frame = self.section("Top Gainers (24h)")
        self.losers_frame = self.section("Top Losers (24h)")
        self.news_frame = self.section("Latest Crypto News")

    def clear(self, frame):
        for w in frame.winfo_children():
            w.destroy()

    def refresh_data(self):
        threading.Thread(target=self.update_data, daemon=True).start()
        self.after(60000, self.refresh_data)  # refresh every 60s

    def update_data(self):
        overview = {}
        gainers, losers = [], []
        news = []

        # Market overview (CoinGecko)
        try:
            overview = get_market_overview()
        except Exception as e:
            print("Overview API error:", e)
            overview = {"Market": "Unavailable"}

        # Top movers (Binance)
        try:
            gainers, losers = get_top_movers()
        except Exception as e:
            print("Movers API error:", e)

        # News (optional)
        try:
            news = get_crypto_news()
        except Exception as e:
            print("News API error:", e)
            news = ["News unavailable"]

        self.after(0, lambda: self.update_ui(
            overview, gainers, losers, news
        ))


    def update_ui(self, overview, gainers, losers, news):
        self.clear(self.market_frame)
        self.clear(self.gainers_frame)
        self.clear(self.losers_frame)
        self.clear(self.news_frame)

        for k, v in overview.items():
            tk.Label(
                self.market_frame,
                text=f"{k.replace('_',' ').title()}: {v}",
                bg="#121212",
                fg="#D0D0D0",
                font=("Segoe UI", 9)
            ).pack(anchor="w")

        for g in gainers:
            tk.Label(
                self.gainers_frame,
                text=f"{g['symbol']}  +{g['priceChangePercent']}%",
                bg="#121212",
                fg="#00FF88",
                font=("Segoe UI", 9)
            ).pack(anchor="w")

        for l in losers:
            tk.Label(
                self.losers_frame,
                text=f"{l['symbol']}  {l['priceChangePercent']}%",
                bg="#121212",
                fg="#FF5555",
                font=("Segoe UI", 9)
            ).pack(anchor="w")

        for n in news:
            tk.Label(
                self.news_frame,
                text="• " + n,
                bg="#121212",
                fg="#BBBBBB",
                wraplength=260,
                justify="left",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=2)
