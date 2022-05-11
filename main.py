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
pd.set_option('display.max_columns', None)  # useful for testing to display full dataframe
sessions_in_year = 365

# tkinter set up
root = Tk()
root.title("Historical Volatility Calculations - Cryptarbitrage")
root.iconbitmap('cryptarbitrage_icon_96px.ico')
root.minsize(400, 200)

# Details frame
details_frame = LabelFrame(root, text="Details", padx=2, pady=2)
details_frame.grid(row=0, column=0, padx=2, pady=2, sticky=NW)
vol_period_label = Label(details_frame, text="HV Periods", font=('Arial', 9, 'bold', 'underline'))
vol_period_label.grid(row=0, column=0, columnspan=2, padx=2, pady=5)
vol_7_day_checked = IntVar()
vol_7_day_checkbox = Checkbutton(details_frame, text='7D', variable=vol_7_day_checked)
vol_7_day_checkbox.grid(row=1, column=0, padx=2, pady=2, sticky=W)
vol_30_day_checked = IntVar()
vol_30_day_checkbox = Checkbutton(details_frame, text='30D', variable=vol_30_day_checked)
vol_30_day_checkbox.grid(row=1, column=1, padx=2, pady=2, sticky=W)
vol_60_day_checked = IntVar()
vol_60_day_checkbox = Checkbutton(details_frame, text='60D', variable=vol_60_day_checked)
vol_60_day_checkbox.grid(row=2, column=0, padx=2, pady=2, sticky=W)
vol_90_day_checked = IntVar()
vol_90_day_checkbox = Checkbutton(details_frame, text='90D', variable=vol_90_day_checked)
vol_90_day_checkbox.grid(row=2, column=1, padx=2, pady=2, sticky=W)
vol_180_day_checked = IntVar()
vol_180_day_checkbox = Checkbutton(details_frame, text='180D', variable=vol_180_day_checked)
vol_180_day_checkbox.grid(row=3, column=0, padx=2, pady=2, sticky=W)
park_vol_label = Label(details_frame, text="Parkinson Vol Comparison", font=('Arial', 9, 'bold', 'underline'))
park_vol_label.grid(row=4, column=0, columnspan=2, padx=2, pady=5)
selected_period = StringVar()
selected_period.set("7D")
period_dropdown = OptionMenu(details_frame, selected_period, "7D", "30D", "60D", "90D", "180D")
period_dropdown.grid(row=5, column=0)
period_dropdown.config(width=10)
include_price_checked = IntVar()
include_price_checkbox = Checkbutton(details_frame, text='Include Underlying Price', variable=include_price_checked)
include_price_checkbox.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=W)

# Chart frames
chart1_frame = LabelFrame(root, text="Historical Volatility", padx=2, pady=2)
chart1_frame.grid(row=0, column=1, rowspan=2, padx=2, pady=2)
chart2_frame = LabelFrame(root, text="Parkinson Vol Comparison", padx=2, pady=2)
chart2_frame.grid(row=2, column=1, padx=2, pady=2)
chart3_frame = LabelFrame(root, text="Underlying Price", padx=2, pady=2)
chart3_frame.grid(row=3, column=1, padx=2, pady=2)

# read in the price data from csv
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
    if vol_7_day_checked.get() == TRUE:
        plot1.plot(df['Date'], df['vol_7_day'], label='7D', color='#1f77b4')
    if vol_30_day_checked.get() == TRUE:
        plot1.plot(df['Date'], df['vol_30_day'], label='30D', color='#ff7f0e')
    if vol_60_day_checked.get() == TRUE:
        plot1.plot(df['Date'], df['vol_60_day'], label='60D', color='#2ca02c')
    if vol_90_day_checked.get() == TRUE:
        plot1.plot(df['Date'], df['vol_90_day'], label='90D', color='#d62728')
    if vol_180_day_checked.get() == TRUE:
        plot1.plot(df['Date'], df['vol_180_day'], label='180D', color='#9467bd')

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
    if selected_period.get() == "7D":
        plot2.plot(df['Date'], df['vol_7_day'], label='7D C2C', color='#1f77b4')
        plot2.plot(df['Date'], df['park_vol_7_day'], label='7D Parkinson', color='#555555')
    if selected_period.get() == "30D":
        plot2.plot(df['Date'], df['vol_30_day'], label='30D C2C', color='#ff7f0e')
        plot2.plot(df['Date'], df['park_vol_30_day'], label='30D Parkinson', color='#555555')
    if selected_period.get() == "60D":
        plot2.plot(df['Date'], df['vol_60_day'], label='60D C2C', color='#2ca02c')
        plot2.plot(df['Date'], df['park_vol_60_day'], label='60D Parkinson', color='#555555')
    if selected_period.get() == "90D":
        plot2.plot(df['Date'], df['vol_90_day'], label='90D C2C', color='#d62728')
        plot2.plot(df['Date'], df['park_vol_90_day'], label='90D Parkinson', color='#555555')
    if selected_period.get() == "180D":
        plot2.plot(df['Date'], df['vol_180_day'], label='180D C2C', color='#9467bd')
        plot2.plot(df['Date'], df['park_vol_180_day'], label='180D Parkinson', color='#555555')
    plot2.set_xlabel('Date')
    plot2.set_ylabel('Volatility (decimal)')
    plot2.set_title('HV - Close To Close (C2C) vs Parkinson')
    plot2.legend()
    plot2.grid(True, alpha=0.25)

    # Underlying price plot
    if include_price_checked.get() == TRUE:
        plot2_b = plot2.twinx()
        plot2_b.plot(df['Date'], df['Close'], label='Closing prices', color='#17becf', linewidth=0.7)
        plot2_b.tick_params(axis='y', labelcolor='#17becf')
        plot2_b.set_ylabel('Underlying Price')

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

    plt.show()


# button that displays the plot
plot_button = Button(master=details_frame,
                     command=plot_charts,
                     height=1,
                     width=18,
                     text="Plot All",
                     bg="#88bb88")

plot_button.grid(row=7, column=0, columnspan=2)

root.mainloop()
