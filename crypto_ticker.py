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
        
        # Create UI
        self.frame = tk.Frame(parent, bg="#1E1E1E", highlightbackground="#2A2A2A",highlightthickness=1, padx=20, pady=20)
        
        # Title
        ttk.Label(self.frame, text=display_name, 
                 font=("Arial", 16, "bold")).pack()
        
        # Price
        self.price_label = tk.Label(self.frame, text="--,---", 
                                    font=("Arial", 40, "bold"))
        self.price_label.pack(pady=10)
        
        # Change
        self.change_label = ttk.Label(self.frame, text="--", 
                                      font=("Arial", 12))
        self.change_label.pack()
    
    def start(self):
        """Start WebSocket connection."""
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
        
        threading.Thread(target=self.ws.run_forever, daemon=True).start()
    
    def stop(self):
        """Stop WebSocket connection."""
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None
    
    def on_message(self, ws, message):
        """Handle price updates."""
        if not self.is_active:
            return
        
        data = json.loads(message)
        price = float(data['c'])
        change = float(data['p'])
        percent = float(data['P'])
        
        # Schedule GUI update on main thread
        self.parent.after(0, self.update_display, price, change, percent)
    
    def update_display(self, price, change, percent):
        """Update the ticker display."""
        if not self.is_active:
            return
        
        color = "green" if change >= 0 else "red"
        self.price_label.config(text=f"{price:,.2f}", fg=color)
        
        sign = "+" if change >= 0 else ""
        self.change_label.config(
            text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",
            foreground=color
        )
    
    def pack(self, **kwargs):
        """Allow easy placement of ticker."""
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        """Hide the ticker."""
        self.frame.pack_forget()
