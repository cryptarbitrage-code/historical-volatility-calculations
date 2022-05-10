from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from volatility_calculations import calculate_historical_vols

# Some chart parameters
chart_size = (12, 4)

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
chart2_frame = LabelFrame(root, text="Chart 2", padx=2, pady=2)
chart2_frame.grid(row=2, column=1, padx=2, pady=2)

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
    plot1.plot(df['Date'], df['vol_7_day'])
    plot1.plot(df['Date'], df['vol_30_day'])
    plot1.plot(df['Date'], df['vol_60_day'])
    plot1.plot(df['Date'], df['vol_90_day'])
    plot1.plot(df['Date'], df['vol_180_day'])
    plot1.set_xlabel('Date')
    plot1.set_ylabel('Volatility (decimal)')
    plot1.set_title('Historical Volatility (close to close)')
    #plot1.legend()
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
