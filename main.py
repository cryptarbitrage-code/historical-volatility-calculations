from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from volatility_calculations import calculate_historical_vols

# Some chart parameters
chart_size = (12, 3)

# other settings
pd.set_option('display.max_columns', None)
sessions_in_year = 365

# tkinter set up
root = Tk()
root.title("Historical Volatility Calculations - Cryptarbitrage")
root.iconbitmap('cryptarbitrage_icon_96px.ico')
root.minsize(400, 200)

# Details frame
details_frame = LabelFrame(root, text="Details", padx=2, pady=2)
details_frame.grid(row=0, column=0, padx=2, pady=2, sticky=NW)
# Chart frames
chart1_frame = LabelFrame(root, text="Historical Volatility", padx=2, pady=2)
chart1_frame.grid(row=0, column=1, rowspan=2, padx=2, pady=2)
chart2_frame = LabelFrame(root, text="Parkinson Vol Comparison", padx=2, pady=2)
chart2_frame.grid(row=2, column=1, padx=2, pady=2)
chart3_frame = LabelFrame(root, text="Underlying Price", padx=2, pady=2)
chart3_frame.grid(row=3, column=1, padx=2, pady=2)

df = pd.read_csv('data/BTC-USD.csv')
df['Date'] = pd.to_datetime(df['Date'])  # change text date to pandas datetime
df = calculate_historical_vols(df, sessions_in_year)
print(df)


def plot_charts():
    # Destroy old charts if any
    for widgets in chart1_frame.winfo_children():
        widgets.destroy()
    for widgets in chart2_frame.winfo_children():
        widgets.destroy()

    # CHART 1: historical volatility: CLOSE TO CLOSE
    # the figure that will contain the plot
    fig1 = Figure(figsize=chart_size, dpi=100)
    # adding the subplot
    plot1 = fig1.add_subplot(111)
    # plotting the graph
    plot1.plot(df['Date'], df['vol_7_day'], label='7D')
    plot1.plot(df['Date'], df['vol_30_day'], label='30D')
    plot1.plot(df['Date'], df['vol_60_day'], label='60D')
    plot1.plot(df['Date'], df['vol_90_day'], label='90D')
    plot1.plot(df['Date'], df['vol_180_day'], label='180D')
    plot1.set_xlabel('Date')
    plot1.set_ylabel('Volatility (decimal)')
    plot1.set_title('Historical Volatility (close to close)')
    plot1.legend()
    plot1.grid(True, alpha=0.25)

    fig1.tight_layout()
    # creating the Tkinter canvas containing the Matplotlib figure
    canvas1 = FigureCanvasTkAgg(fig1, master=chart1_frame)
    canvas1.draw()
    # placing the canvas on the Tkinter window
    canvas1.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas1, chart1_frame)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas1.get_tk_widget().pack()

    # CHART 2: CLOSE TO CLOSE vs Parkinson
    # the figure that will contain the plot
    fig2 = Figure(figsize=chart_size, dpi=100)
    # adding the subplot
    plot2 = fig2.add_subplot(111)
    # plotting the graph
    plot2.plot(df['Date'], df['vol_30_day'], label='30D C2C')
    plot2.plot(df['Date'], df['park_vol_30_day'], label='30D Parkinson')
    plot2.set_xlabel('Date')
    plot2.set_ylabel('Volatility (decimal)')
    plot2.set_title('HV - Close To Close (C2C) vs Parkinson')
    plot2.legend()
    plot2.grid(True, alpha=0.25)

    fig2.tight_layout()
    # creating the Tkinter canvas containing the Matplotlib figure
    canvas2 = FigureCanvasTkAgg(fig2, master=chart2_frame)
    canvas2.draw()
    # placing the canvas on the Tkinter window
    canvas2.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas2, chart2_frame)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas2.get_tk_widget().pack()

    # CHART 3: Price chart
    # the figure that will contain the plot
    fig3 = Figure(figsize=chart_size, dpi=100)
    # adding the subplot
    plot3 = fig3.add_subplot(111)

    # plotting the graph
    plot3.plot(df['Date'], df['Close'], label='Closing prices')
    plot3.set_xlabel('Date')
    plot3.set_ylabel('Price')
    plot3.set_title('Underlying Price')
    plot3.legend()
    plot3.grid(True, alpha=0.25)

    fig3.tight_layout()
    # creating the Tkinter canvas containing the Matplotlib figure
    canvas3 = FigureCanvasTkAgg(fig3, master=chart3_frame)
    canvas3.draw()
    # placing the canvas on the Tkinter window
    canvas3.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas3, chart3_frame)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas3.get_tk_widget().pack()

    plt.show()


# button that displays the plot
plot_button = Button(master=details_frame,
                     command=plot_charts,
                     height=1,
                     width=18,
                     text="Plot",
                     bg="#88bb88")

plot_button.grid(row=3, column=1)

root.mainloop()
