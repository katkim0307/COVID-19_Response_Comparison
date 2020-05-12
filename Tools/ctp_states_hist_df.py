import pandas as pd


def set_ctp_states_hist_df(url):
    # Read COVID Tracking Project US States COVID-19 Accumulative Data
    ctp_states_hist_df = pd.read_json(url, dtype={'fips': object})[
        ['date', 'state', 'fips', 'positive', 'death', 'total']
    ]

    # Removing Palau (PW/70), Guam (GU/66), Northern Mariana Islands (MP/69),
    # American Samoa (AS/60), Hawaii (HI/15), Puerto Rico (PR/72), and Virgin Islnads (VI/78)
    ctp_states_hist_df = ctp_states_hist_df[
        (ctp_states_hist_df['fips'] != '70') &
        (ctp_states_hist_df['fips'] != '66') &
        (ctp_states_hist_df['fips'] != '69') &
        (ctp_states_hist_df['fips'] != '60') &
        (ctp_states_hist_df['fips'] != '15') &
        (ctp_states_hist_df['fips'] != '72') &
        (ctp_states_hist_df['fips'] != '78')
        ]

    # Renaming the `total` to `test`
    ctp_states_hist_df.rename(columns={'total': 'test'}, inplace=True)

    # Converting 'positive', 'death', and 'test' Dtype to int
    ctp_states_hist_df.update(ctp_states_hist_df[['positive', 'death', 'test']].fillna(0).astype(int))

    # Sorting the dataframe by 'date'
    ctp_states_hist_df = ctp_states_hist_df.sort_values(by=['date'], ignore_index=True)

    # Creating a new column, 'datetime' that converts 'date' from dtype: int to the Dtype: str of datetime
    ctp_states_hist_df['datetime'] = pd.to_datetime(ctp_states_hist_df['date'].astype(str), format='%Y-%m-%d')

    # Converting the Dtype to datetime
    ctp_states_hist_df['datetime'] = pd.to_datetime(ctp_states_hist_df['datetime'])

    return ctp_states_hist_df
