import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class CandleChart(tk.Frame):
    def __init__(self, parent, title="Chart"):
        super().__init__(parent, bg="#000000") 

        self.title = title
        self.data = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
        self.fig = Figure(figsize=(6, 4), dpi=100, facecolor="black", edgecolor="black")
        self.ax = self.fig.add_subplot(111)

        mc = mpf.make_marketcolors(
            up='lime',        
            down='red',       
            wick={'up':'lime', 'down':'red'},  
            edge={'up':'lime', 'down':'red'},  
            volume='inherit'  
        )

        self.style = mpf.make_mpf_style(
            base_mpf_style="nightclouds",
            marketcolors=mc,
            facecolor="black",         
            edgecolor="black",
            gridcolor="#333333",       
            gridstyle="-",
            y_on_right=False,
            rc={
                'figure.facecolor': 'black', 
                'axes.facecolor': 'black',   
                'axes.edgecolor': "#1E1E1E",
                'axes.labelcolor': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white',
                'text.color': 'white',
                'grid.color': '#333333',
            }
        )


        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_chart(self, df):
        """df must be a pandas DataFrame with datetime index."""
        if df.empty:
            return
    
        self.data = df
    
        self.ax.clear()
        
        self.ax.set_facecolor('black')

        # Plot 
        mpf.plot(
            df,
            type="candle",
            ax=self.ax,
            style=self.style,
            volume=False,
            warn_too_much_data=150, 
        )
        
        # Manual Text Styling
        self.ax.set_ylabel("Price", color='white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        
        current_title = f"{self.title} - Close: {df['Close'].iloc[-1]:.2f}"
        self.ax.set_title(current_title, color='white')
        
        xfmt = mdates.DateFormatter('%H:%M')
        self.ax.xaxis.set_major_formatter(xfmt)
        
        self.fig.tight_layout()
        self.canvas.draw()