import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
sessions_in_year = 365

df = pd.read_csv('data/BTC-USD.csv')
df['Date'] = pd.to_datetime(df['Date'])
print(df)

# calculate first log returns using the open
log_returns = []
log_returns.append(np.log(df.loc[0, 'Close']/df.loc[0, 'Open']))
print(log_returns)
# calculate all but first log returns using close to close
for index in range(len(df)-1):
    log_returns.append(np.log(df.loc[index + 1, 'Close']/df.loc[index, 'Close']))
df = df.assign(log_returns=log_returns)

print(df)

# calculate the 7-day standard deviation
seven_day_sd = [np.nan] * 6
for index in range(len(df)-6):
    seven_day_sd.append(np.std(df.loc[index:index + 6, 'log_returns'], ddof=1))
df = df.assign(seven_day_sd=seven_day_sd)

print(df)
