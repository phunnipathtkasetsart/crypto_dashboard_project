import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading

class CryptoTicker:
    """Reusable ticker component for any cryptocurrency."""
    
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws = None
        
        # ---- Main card ----
        self.frame = tk.Frame(
            parent,
            bg="#000000",
            highlightbackground="#2A2A2A",   # border color
            highlightthickness=1,
            padx=18,
            pady=14,
        )

        # ---- Left bar ----
        self.accent = tk.Frame(self.frame, bg="#2ECC71", width=4)
        self.accent.pack(side="left", fill="y", padx=(0, 12),pady=0)
        self.accent2 = tk.Frame(self.frame, bg="#000000", width=4)
        self.accent2.pack(side="right", fill="y", padx=(0, 190),pady=0)
        # ---- Title ----
        self.title_label = tk.Label(
            self.frame,
            text=display_name,
            bg="#000000",
            fg="#E0E0E0",
            font=("Segoe UI", 14, "bold")
        )
        self.title_label.pack(anchor="w")

        # ---- price ----
        self.price_label = tk.Label(
            self.frame,
            text="--,---",
            bg="#000000",
            fg="#E0E0E0",
            font=("Segoe UI", 28, "bold")
        )
        self.price_label.pack(anchor="w", pady=(6, 2))

        # ---- change ----
        self.change_label = tk.Label(
            self.frame,
            text="--",
            bg="#000000",
            fg="#A0A0A0",
            font=("Segoe UI", 11)
        )
        self.change_label.pack(anchor="w")

    # Sockets

    def start(self):
        if self.is_active:
            return
        
        self.is_active = True
        ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"
        
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=lambda ws, err: print(f"{self.symbol} error: {err}"),
            on_close=lambda ws, s, m: print(f"{self.symbol} closed"),
            on_open=lambda ws: print(f"{self.symbol} connected")
        )
        # Solution: Always use threading
        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def stop(self):
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None

    # ----------------- UI updates -----------------
    def on_message(self, ws, message):
        if not self.is_active:
            return
        
        data = json.loads(message)
        price = float(data['c'])
        change = float(data['p'])
        percent = float(data['P'])
        
        self.parent.after(0, self.update_display, price, change, percent)

    def update_display(self, price, change, percent):
        if not self.is_active:
            return
        
        # Green/up or Red/down
        up = change >= 0
        color = "#2ECC71" if up else "#E74C3C"

        # Update accent bar
        self.accent.configure(bg=color)

        # Large price text
        self.price_label.config(text=f"{price:,.2f}", fg=color)

        # Smaller change text
        sign = "+" if up else ""
        self.change_label.config(
            text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",
            fg=color
        )

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        self.frame.pack_forget()
