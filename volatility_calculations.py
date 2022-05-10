import numpy as np


def calculate_historical_vols(df, sessions_in_year):
    # calculate first log returns using the open
    log_returns = []
    log_returns.append(np.log(df.loc[0, 'Close'] / df.loc[0, 'Open']))
    # calculate all but first log returns using close to close
    for index in range(len(df) - 1):
        log_returns.append(np.log(df.loc[index + 1, 'Close'] / df.loc[index, 'Close']))
    df = df.assign(log_returns=log_returns)

    # log returns squared - using high and low - for Parkinson volatility
    high_low_log_returns_squared = []
    for index in range(len(df)):
        high_low_log_returns_squared.append(np.log(df.loc[index, 'High'] / df.loc[index, 'Low']) ** 2)
    df = df.assign(high_low_log_returns_squared=high_low_log_returns_squared)

    # calculate the 7-day standard deviation and vol
    if len(df) > 6:
        sd_7_day = [np.nan] * 6
        vol_7_day = [np.nan] * 6
        park_vol_7_day = [np.nan] * 6
        for index in range(len(df) - 6):
            sd = np.std(df.loc[index:index + 6, 'log_returns'], ddof=1)
            sd_7_day.append(sd)
            vol_7_day.append(sd * np.sqrt(sessions_in_year))
            park_vol_7_day.append(np.sqrt(
                (1 / (4 * 7 * np.log(2)) * sum(df.loc[index:index + 6, 'high_low_log_returns_squared']))) * np.sqrt(
                sessions_in_year))
        df = df.assign(sd_7_day=sd_7_day)
        df = df.assign(vol_7_day=vol_7_day)
        df = df.assign(park_vol_7_day=park_vol_7_day)

    # calculate the 30-day standard deviation and vol
    if len(df) > 29:
        sd_30_day = [np.nan] * 29
        vol_30_day = [np.nan] * 29
        park_vol_30_day = [np.nan] * 29
        for index in range(len(df) - 29):
            sd = np.std(df.loc[index:index + 29, 'log_returns'], ddof=1)
            sd_30_day.append(sd)
            vol_30_day.append(sd * np.sqrt(sessions_in_year))
            park_vol_30_day.append(np.sqrt(
                (1 / (4 * 30 * np.log(2)) * sum(df.loc[index:index + 29, 'high_low_log_returns_squared']))) * np.sqrt(
                sessions_in_year))
        df = df.assign(sd_30_day=sd_30_day)
        df = df.assign(vol_30_day=vol_30_day)
        df = df.assign(park_vol_30_day=park_vol_30_day)

    # calculate the 60-day standard deviation and vol
    if len(df) > 59:
        sd_60_day = [np.nan] * 59
        vol_60_day = [np.nan] * 59
        park_vol_60_day = [np.nan] * 59
        for index in range(len(df) - 59):
            sd = np.std(df.loc[index:index + 59, 'log_returns'], ddof=1)
            sd_60_day.append(sd)
            vol_60_day.append(sd * np.sqrt(sessions_in_year))
            park_vol_60_day.append(np.sqrt(
                (1 / (4 * 60 * np.log(2)) * sum(df.loc[index:index + 59, 'high_low_log_returns_squared']))) * np.sqrt(
                sessions_in_year))
        df = df.assign(sd_60_day=sd_60_day)
        df = df.assign(vol_60_day=vol_60_day)
        df = df.assign(park_vol_60_day=park_vol_60_day)

    # calculate the 90-day standard deviation and vol
    if len(df) > 89:
        sd_90_day = [np.nan] * 89
        vol_90_day = [np.nan] * 89
        park_vol_90_day = [np.nan] * 89
        for index in range(len(df) - 89):
            sd = np.std(df.loc[index:index + 89, 'log_returns'], ddof=1)
            sd_90_day.append(sd)
            vol_90_day.append(sd * np.sqrt(sessions_in_year))
            park_vol_90_day.append(np.sqrt(
                (1 / (4 * 90 * np.log(2)) * sum(df.loc[index:index + 89, 'high_low_log_returns_squared']))) * np.sqrt(
                sessions_in_year))
        df = df.assign(sd_90_day=sd_90_day)
        df = df.assign(vol_90_day=vol_90_day)
        df = df.assign(park_vol_90_day=park_vol_90_day)

    # calculate the 180-day standard deviation and vol
    if len(df) > 179:
        sd_180_day = [np.nan] * 179
        vol_180_day = [np.nan] * 179
        park_vol_180_day = [np.nan] * 179
        for index in range(len(df) - 179):
            sd = np.std(df.loc[index:index + 179, 'log_returns'], ddof=1)
            sd_180_day.append(sd)
            vol_180_day.append(sd * np.sqrt(sessions_in_year))
            park_vol_180_day.append(np.sqrt(
                (1 / (4 * 180 * np.log(2)) * sum(df.loc[index:index + 179, 'high_low_log_returns_squared']))) * np.sqrt(
                sessions_in_year))
        df = df.assign(sd_180_day=sd_180_day)
        df = df.assign(vol_180_day=vol_180_day)
        df = df.assign(park_vol_180_day=park_vol_180_day)

        return df
