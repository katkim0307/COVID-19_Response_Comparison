import pandas as pd


def set_ctp_states_now_df(url):
    # Read COVID Tracking Project US States COVID-19 Current Data
    ctp_states_now_df = pd.read_json(url, dtype={'fips': object})[
        ['state', 'fips', 'positive', 'death', 'total']
    ]

    # Removing Palau (PW/70), Guam (GU/66), Northern Mariana Islands (MP/69),
    # American Samoa (AS/60), Hawaii (HI/15), Puerto Rico (PR/72), and Virgin Islnads (VI/78)
    ctp_states_now_df = ctp_states_now_df[
        (ctp_states_now_df['fips'] != '70') &
        (ctp_states_now_df['fips'] != '66') &
        (ctp_states_now_df['fips'] != '69') &
        (ctp_states_now_df['fips'] != '60') &
        (ctp_states_now_df['fips'] != '15') &
        (ctp_states_now_df['fips'] != '72') &
        (ctp_states_now_df['fips'] != '78')
        ]

    # Renaming the `total` to `test`
    ctp_states_now_df.rename(columns={'total': 'test'}, inplace=True, )

    return ctp_states_now_df
