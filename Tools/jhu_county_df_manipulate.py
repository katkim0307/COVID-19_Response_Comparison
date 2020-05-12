import pandas as pd


def manipulate_jhu_county_df(df_to_fix, df_to_manipulate_with):
    # Modifying NYC Counties Data because all NYC counties data is aggregated
    # under 'New York' only and not the rest boroughs
    nyc_idx = df_to_fix.index[
        (df_to_fix['Admin2'] == 'Bronx') | \
        ((df_to_fix['Admin2'] == 'Kings') & (df_to_fix['Province_State'] == 'New York')) | \
        (df_to_fix['Admin2'] == 'Queens') | \
        ((df_to_fix['Admin2'] == 'Richmond') & (df_to_fix['Province_State'] == 'New York'))
        ].tolist()

    ny_idx = df_to_fix.index[(df_to_fix['Admin2'] == 'New York')].tolist()

    # copying 'new york' county value to all other boroughs
    df_to_fix.loc[nyc_idx, '1/22/20':] = df_to_fix.loc[ny_idx, '1/22/20':].values

    # Fixing issues with NaN FIPS in the jhu_county_df
    missing_idx = df_to_fix[
        (df_to_fix['Admin2'] == 'Central Utah') | \
        (df_to_fix['Admin2'] == 'Southeast Utah') | \
        (df_to_fix['Admin2'] == 'Southwest Utah') | \
        (df_to_fix['Admin2'] == 'TriCounty') | \
        (df_to_fix['Admin2'] == 'Michigan Department of Corrections (MDOC)') | \
        (df_to_fix['Admin2'] == 'Federal Correctional Institution (FCI)') | \
        ((df_to_fix['Admin2'] == 'Morgan') & (df_to_fix['Province_State'] == 'Utah')) | \
        ((df_to_fix['Admin2'] == 'Rich') & (df_to_fix['Province_State'] == 'Utah')) | \
        (df_to_fix['Admin2'] == 'Cache') | \
        ((df_to_fix['Admin2'] == 'Beaver') & (df_to_fix['Province_State'] == 'Utah')) | \
        (df_to_fix['Admin2'] == 'Millard') | \
        ((df_to_fix['Admin2'] == 'Iron') & (df_to_fix['Province_State'] == 'Utah')) | \
        (df_to_fix['Admin2'] == 'Uintah)') | \
        ((df_to_fix['Admin2'] == 'Garfield') & (df_to_fix['Province_State'] == 'Utah')) | \
        ((df_to_fix['Admin2'] == 'Kane') & (df_to_fix['Province_State'] == 'Utah')) | \
        ((df_to_fix['Admin2'] == 'Carbon') & (df_to_fix['Province_State'] == 'Utah')) | \
        ((df_to_fix['Admin2'] == 'Washington') & (df_to_fix['Province_State'] == 'Utah')) | \
        (df_to_fix['Admin2'] == 'Duchesne') | \
        (df_to_fix['Admin2'] == 'Emery') | \
        ((df_to_fix['Admin2'] == 'Grand') & (df_to_fix['Province_State'] == 'Utah')) | \
        (df_to_fix['Admin2'] == 'Juab') | \
        ((df_to_fix['Admin2'] == 'Sevier') & (df_to_fix['Province_State'] == 'Utah')) | \
        (df_to_fix['Admin2'] == 'Sanpete') | \
        ((df_to_fix['Admin2'] == 'Piute') & (df_to_fix['Province_State'] == 'Utah')) | \
        ((df_to_fix['Admin2'] == 'Wayne') & (df_to_fix['Province_State'] == 'Utah')) | \
        ((df_to_fix['Admin2'] == 'Beaver') & (df_to_fix['Province_State'] == 'Utah')) | \
        (df_to_fix['Admin2'] == 'Daggett')
        ].index

    df_to_fix.drop(missing_idx, inplace=True)

    for i in df_to_fix.index:
        if df_to_fix.loc[i, 'Admin2'] == 'Dukes and Nantucket':
            df_to_fix.at[i, 'FIPS'] = '25019'

        elif df_to_fix.loc[i, 'Admin2'] == 'Weber-Morgan':
            df_to_fix.at[i, 'FIPS'] = '49057'

        elif df_to_fix.loc[i, 'Admin2'] == 'Bear River':
            df_to_fix.at[i, 'FIPS'] = '49003'

        elif df_to_fix.loc[i, 'Admin2'] == 'Kansas City':
            df_to_fix.at[i, 'FIPS'] = '29095'

    # Converting individual date colums into rows a.k.a Transpose
    jhu_county_df = df_to_fix.melt(id_vars=['Admin2', 'Province_State', 'FIPS', 'Lat', 'Long_'],
                                   var_name='Date',
                                   value_name='Cases')

    jhu_county_df['FIPS'] = jhu_county_df['FIPS'].astype(int).astype(object)
    jhu_county_df['datetime'] = pd.to_datetime(jhu_county_df['Date'].astype(str), format='%m/%d/%y')
    jhu_county_df['datetime'] = pd.to_datetime(jhu_county_df['datetime'])

    # Modifying Utah Counties Data because they are using 'Central', 'Southeast', 'Southwest', and
    # 'TriCounty' instead of specific counties.  Going to `.concat` NYTimes Utah County Data
    df_to_manipulate_with.drop('deaths', inplace=True, axis=1)

    missing_ut_county_df = df_to_manipulate_with[
        ((df_to_manipulate_with['county'] == 'Morgan') & (df_to_manipulate_with['state'] == 'Utah')) | \
        ((df_to_manipulate_with['county'] == 'Rich') & (df_to_manipulate_with['state'] == 'Utah')) | \
        (df_to_manipulate_with['county'] == 'Cache') | \
        ((df_to_manipulate_with['county'] == 'Beaver') & (df_to_manipulate_with['state'] == 'Utah')) | \
        (df_to_manipulate_with['county'] == 'Millard') | \
        ((df_to_manipulate_with['county'] == 'Iron') & (df_to_manipulate_with['state'] == 'Utah')) | \
        (df_to_manipulate_with['county'] == 'Uintah)') | \
        ((df_to_manipulate_with['county'] == 'Garfield') & (df_to_manipulate_with['state'] == 'Utah')) | \
        ((df_to_manipulate_with['county'] == 'Kane') & (df_to_manipulate_with['state'] == 'Utah')) | \
        ((df_to_manipulate_with['county'] == 'Carbon') & (df_to_manipulate_with['state'] == 'Utah')) | \
        ((df_to_manipulate_with['county'] == 'Washington') & (df_to_manipulate_with['state'] == 'Utah')) | \
        (df_to_manipulate_with['county'] == 'Duchesne') | \
        (df_to_manipulate_with['county'] == 'Emery') | \
        ((df_to_manipulate_with['county'] == 'Grand') & (df_to_manipulate_with['state'] == 'Utah')) | \
        (df_to_manipulate_with['county'] == 'Juab') | \
        ((df_to_manipulate_with['county'] == 'Sevier') & (df_to_manipulate_with['state'] == 'Utah')) | \
        (df_to_manipulate_with['county'] == 'Sanpete') | \
        ((df_to_manipulate_with['county'] == 'Piute') & (df_to_manipulate_with['state'] == 'Utah')) | \
        ((df_to_manipulate_with['county'] == 'Wayne') & (df_to_manipulate_with['state'] == 'Utah')) | \
        ((df_to_manipulate_with['county'] == 'Beaver') & (df_to_manipulate_with['state'] == 'Utah')) | \
        (df_to_manipulate_with['county'] == 'Daggett')
        ]

    jhu_county_df = pd.concat([jhu_county_df, missing_ut_county_df.rename(columns={
        'date': 'Date',
        'county': 'Admin2',
        'state': 'Province_State',
        'fips': 'FIPS',
        'cases': 'Cases',
        'datetime': 'datetime', })], ignore_index=True)

    jhu_county_df = jhu_county_df.sort_values(by=['datetime'], ignore_index=True)

    return jhu_county_df
