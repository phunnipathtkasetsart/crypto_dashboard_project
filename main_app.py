import tkinter as tk
from tkinter import ttk

from Tickers.btc_ticker import BTCTicker
from Tickers.eth_ticker import ETHTicker
from Tickers.bnb_ticker import BNBTicker
from Tickers.sol_ticker import SOLTicker
from Tickers.ada_ticker import ADATicker
from Tickers.xrp_ticker import XRPTicker
from Tickers.doge_ticker import DOGETicker
from Tickers.dot_ticker import DOTTicker
from Tickers.link_ticker import LINKTicker
from Tickers.ltc_ticker import LTCTicker
from Tickers.shib_ticker import SHIBTicker


class MultiTickerApp:
    def __init__(self, root):
        self.root = root
        root.title("Crypto Dashboard")
        root.geometry("1200x600")

        self.tickers = []


        ## Scroll ##


        left_container = tk.Frame(root, bg="#1E1E1E")
        left_container.pack(side="left", fill="y")

        # Canvas for scrolling
        self.canvas = tk.Canvas(left_container, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(side="left", fill="y", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Connect scrollbar ↔ canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Inner frame inside canvas
        self.left_panel = tk.Frame(self.canvas, bg="#1E1E1E")
        self.canvas.create_window((0, 0), window=self.left_panel, anchor="nw")

        # Auto scroll region
        self.left_panel.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Allow scroll with mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        
        ## Scroll ##


        self.center_panel = tk.Frame(root, bg="#000000")
        self.center_panel.pack(side="left", fill="both", expand=True)

        #Add tickers
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
        """Apply Figma-style dark theme to a ticker frame."""
        ticker_frame.configure(bg="#1E1E1E")

        for widget in ticker_frame.winfo_children():
            try:
                widget.configure(bg="#1E1E1E", fg="#D0D0D0", font=("Segoe UI", 12))
            except:
                pass

        ticker_frame.configure(
            highlightbackground="#2A2A2A",
            highlightthickness=1,
            bd=0,
            padx=10,
            pady=10
        )
    
    def add_ticker(self, parent, TickerClass):
        ticker = TickerClass(parent)
        ticker.pack(fill="x", pady=6, padx=6)

        self.style_ticker(ticker.frame)

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
