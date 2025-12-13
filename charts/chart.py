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
        self.data = pd.DataFrame(
            columns=["Open", "High", "Low", "Close", "Volume"]
        )

        self.fig = Figure(
            figsize=(6, 4),
            dpi=100,
            facecolor="#0E0E0E",   # outer panel
            edgecolor="#2A2A2A"
        )

        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#000000")  # inner plot area

        self.fig.subplots_adjust(
            left=0,
            right=1,
            top=1,
            bottom=0
        )

        mc = mpf.make_marketcolors(
            up='lime',
            down='red',
            wick={'up': 'lime', 'down': 'red'},
            edge={'up': 'lime', 'down': 'red'},
            volume='inherit'
        )

        self.style = mpf.make_mpf_style(
            base_mpf_style="nightclouds",
            marketcolors=mc,
            facecolor="#000000",
            edgecolor="#2A2A2A",
            gridcolor="#2A2A2A",
            gridstyle="-",
            y_on_right=False,
            rc={
                'figure.facecolor': '#0E0E0E',
                'axes.facecolor': '#000000',
                'axes.edgecolor': '#2E2E2E',
                'axes.labelcolor': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white',
                'text.color': 'white',
                'grid.color': '#2A2A2A',
            }
        )

        # Grid 
        self.ax.grid(
            True,
            which='major',
            linestyle='-',
            linewidth=0.6,
            color='#2A2A2A'
        )

        # Axis border
        for spine in self.ax.spines.values():
            spine.set_color("#2E2E2E")
            spine.set_linewidth(1.2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True,
            padx=6,
            pady=6
        )

    def update_chart(self, df: pd.DataFrame):
        """df must be a pandas DataFrame with datetime index"""
        if df.empty:
            return

        self.data = df
        self.ax.clear()
        self.ax.set_facecolor("#000000")

        self.ax.grid(
            True,
            which='major',
            linestyle='-',
            linewidth=0.6,
            color='#2A2A2A'
        )

        for spine in self.ax.spines.values():
            spine.set_color("#2E2E2E")
            spine.set_linewidth(1.2)


        mpf.plot(
            df,
            type="candle",
            ax=self.ax,
            style=self.style,
            volume=False,
            warn_too_much_data=150,
            show_nontrading=True
        )

        self.ax.set_ylabel("Price", color='white', fontsize=9)
        self.ax.tick_params(
            axis='both',
            colors='white',
            labelsize=9,
            pad=6
        )

        # Title (Excel-style header)
        close_price = df["Close"].iloc[-1]
        self.ax.set_title(
            f"{self.title}   Close: {close_price:.4f}",
            color='white',
            fontsize=11,
            pad=12,
            loc="left"
        )

        # Time formatter
        self.ax.xaxis.set_major_formatter(
            mdates.DateFormatter('%H:%M')
        )

        self.fig.tight_layout(pad=1.5)
        self.canvas.draw_idle()
