import pandas as pd


def set_ctp_us_hist_df(url):
    # COVID Tracking Project US COVID-19 Accumulative Data
    ctp_us_hist_df = pd.read_json(url, dtype={'fips': object, 'date': object})[
        ['date', 'positive', 'death', 'total']
    ]

    # Renaming the `total` to `test`
    ctp_us_hist_df.rename(columns={'total': 'test'}, inplace=True)

    # Sorting the dataframe by 'date'
    ctp_us_hist_df = ctp_us_hist_df.sort_values(by=['date'], ignore_index=True)

    # Creating a new column, 'datetime' that converts 'date' from dtype: int to the Dtype: str of datetime
    ctp_us_hist_df['datetime'] = pd.to_datetime(ctp_us_hist_df['date'].astype(str), format='%Y-%m-%d')

    # Converting the Dtype to datetime
    ctp_us_hist_df['datetime'] = pd.to_datetime(ctp_us_hist_df['datetime'])

    return ctp_us_hist_df
