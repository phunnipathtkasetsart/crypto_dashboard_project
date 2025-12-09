import tkinter as tk
from tkinter import ttk

# Import all ticker files
from crypto_ticker import CryptoTicker
from tickers.btc_ticker import BTCTicker
from tickers.eth_ticker import ETHTicker
from tickers.bnb_ticker import BNBTicker
from tickers.sol_ticker import SOLTicker
from tickers.ada_ticker import ADATicker
from tickers.xrp_ticker import XRPTicker
from tickers.doge_ticker import DOGETicker
from tickers.dot_ticker import DOTTicker
from tickers.link_ticker import LINKTicker
from tickers.ltc_ticker import LTCTicker
from tickers.shib_ticker import SHIBTicker


class MultiTickerApp:
    def __init__(self, root):
        self.root = root
        root.title("Crypto Dashboard")
        root.geometry("1200x600")

        self.tickers = []
        self.sol_visible = False

        # Scrolls
        left_container = tk.Frame(root, bg="#1E1E1E")
        left_container.pack(side="left", fill="y")
        self.canvas = tk.Canvas(left_container, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(side="left", fill="y", expand=True)
        scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.left_panel = tk.Frame(self.canvas, bg="#1E1E1E")
        self.canvas.create_window((0, 0), window=self.left_panel, anchor="nw")
        self.left_panel.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.center_panel = tk.Frame(root, bg="#000000")
        self.center_panel.pack(side="left", fill="both", expand=True)


        # Control pannel
        control_frame = ttk.Frame(root, padding=10)
        control_frame.pack(fill=tk.X)

        # Button to show/hide SOL chart on the right
        self.sol_btn = ttk.Button(
            control_frame,
            text="Show SOL/USDT",
            command=self.toggle_sol
        )
        self.sol_btn.pack()

        # Create the SOL chart ticker, but don't show it yet
        self.sol_ticker = CryptoTicker(self.center_panel, "solusdt", "SOL/USDT")



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

    def toggle_sol(self):
        if self.sol_visible:
            self.sol_ticker.stop()
            self.sol_ticker.pack_forget()
            self.sol_btn.config(text="Show SOL/USDT")
            self.sol_visible = False
        else:
            self.sol_ticker.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.sol_ticker.start()
            self.sol_btn.config(text="Hide SOL/USDT")
            self.sol_visible = True


    def add_ticker(self, parent, TickerClass):
        ticker = TickerClass(parent)   # Create ticker object
        ticker.pack(fill="x", pady=6, padx=6)

        self.style_ticker(ticker.frame)  # Style it

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
