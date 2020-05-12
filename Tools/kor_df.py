import pandas as pd


def set_kor_df(input_data_filepath, sheet_name):
    kor_cov19_df = pd.read_excel(input_data_filepath, sheet_name)
    kor_cov19_df['datetime'] = kor_cov19_df['Date'].copy()
    kor_cov19_df['Date'] = kor_cov19_df['Date'].astype(str)

    if sheet_name == 'covid_19_daily_province':
        kor_cov19_df.update(
            kor_cov19_df[['Confirm_New', 'Confirm_Tot', 'Death_New', 'Death_Tot']].fillna(0, inplace=True))

    return kor_cov19_df
