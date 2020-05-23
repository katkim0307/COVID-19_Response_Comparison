import pandas as pd


def manipulate_jhu_county_df(df_to_fix, df_to_manip_with1, df_to_manip_with2):
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

    # Converting individual date colums into rows a.k.a Melting
    jhu_county_df = df_to_fix.melt(id_vars=['Admin2', 'Province_State', 'FIPS', 'Lat', 'Long_'],
                                   var_name='Date',
                                   value_name='Cases')

    jhu_county_df['FIPS'] = jhu_county_df['FIPS'].astype(int).astype(object)
    jhu_county_df['datetime'] = pd.to_datetime(jhu_county_df['Date'].astype(str), format='%m/%d/%y')
    jhu_county_df['datetime'] = pd.to_datetime(jhu_county_df['datetime'])

    # ---------------------------#
    #     NYC COUNTY ISSUES      #
    #     df_to_manip_with_1     #
    # ---------------------------#
    # Modifying NYC Counties Data because all NYC counties data is aggregated
    # under 'New York' only and not the rest boroughs
    nyc_idx = jhu_county_df.index[
        (jhu_county_df['Admin2'] == 'Bronx') | \
        ((jhu_county_df['Admin2'] == 'Kings') & (jhu_county_df['Province_State'] == 'New York')) | \
        (jhu_county_df['Admin2'] == 'New York') | \
        (jhu_county_df['Admin2'] == 'Queens') | \
        ((jhu_county_df['Admin2'] == 'Richmond') & (jhu_county_df['Province_State'] == 'New York'))
        ].tolist()

    jhu_county_df.drop(nyc_idx, inplace=True)

    df_to_manip_with1.rename(columns={'timestamp': 'date',
                                      'bronx': 'Bronx',
                                      'brooklyn': 'Kings',
                                      'queens': 'Queens',
                                      'manhattan': 'New York',
                                      'staten_island': 'Richmond'},
                             inplace=True)

    df_to_manip_with1['New York'] = df_to_manip_with1['Queens'] + df_to_manip_with1['unknown']
    df_to_manip_with1['date'] = pd.to_datetime(df_to_manip_with1['date'], infer_datetime_format=True).astype(str)
    df_to_manip_with1['date'] = df_to_manip_with1['date'].str[:-9]
    df_to_manip_with1.drop(['total', 'unknown'], inplace=True, axis=1)

    thecity_cases_df = df_to_manip_with1[df_to_manip_with1['type'] == 'cases'].copy()
    thecity_cases_df.drop('type', inplace=True, axis=1)

    thecity_cases_transposed_df = thecity_cases_df.set_index('date').transpose(copy=True).copy()
    thecity_cases_transposed_df['FIPS'] = ['36005', '36047', '36061', '36081', '36085']
    thecity_cases_transposed_df['Admin2'] = ['Bronx', 'Kings', 'New York', 'Queens', 'Richmond']
    thecity_cases_transposed_df['Province_State'] = ['New York', 'New York', 'New York', 'New York', 'New York']
    thecity_cases_transposed_df = thecity_cases_transposed_df[
        ['FIPS', 'Admin2', 'Province_State'] + [col for col in thecity_cases_transposed_df if
                                                col not in ['FIPS', 'Admin2', 'Province_State']]]
    thecity_cases_transposed_df.reset_index(drop=True, inplace=True)
    thecity_cases_transposed_df = thecity_cases_transposed_df.rename_axis(None)

    thecity_cases_df = thecity_cases_transposed_df.melt(id_vars=['FIPS', 'Admin2', 'Province_State'],
                                                        var_name='Date', value_name='Cases')

    thecity_cases_df['datetime'] = pd.to_datetime(thecity_cases_df['Date'])

    jhu_county_df = pd.concat([jhu_county_df, thecity_cases_df.rename(columns={
        'Admin2': 'Admin2',
        'Province_State': 'Province_State',
        'FIPS': 'FIPS',
        'Date': 'Date',
        'Cases': 'Cases',
        'datetime': 'datetime', })], ignore_index=True)

    # ---------------------------#
    #     Utah COUNTY ISSUES     #
    #     df_to_manip_with_2     #
    # ---------------------------#
    # Modifying Utah Counties Data because they are using 'Central', 'Southeast', 'Southwest', and
    # 'TriCounty' instead of specific counties.  Going to `.concat` NYTimes Utah County Data
    df_to_manip_with2.drop('deaths', inplace=True, axis=1)

    missing_ut_county_df = df_to_manip_with2[
        ((df_to_manip_with2['county'] == 'Morgan') & (df_to_manip_with2['state'] == 'Utah')) | \
        ((df_to_manip_with2['county'] == 'Rich') & (df_to_manip_with2['state'] == 'Utah')) | \
        (df_to_manip_with2['county'] == 'Cache') | \
        ((df_to_manip_with2['county'] == 'Beaver') & (df_to_manip_with2['state'] == 'Utah')) | \
        (df_to_manip_with2['county'] == 'Millard') | \
        ((df_to_manip_with2['county'] == 'Iron') & (df_to_manip_with2['state'] == 'Utah')) | \
        (df_to_manip_with2['county'] == 'Uintah)') | \
        ((df_to_manip_with2['county'] == 'Garfield') & (df_to_manip_with2['state'] == 'Utah')) | \
        ((df_to_manip_with2['county'] == 'Kane') & (df_to_manip_with2['state'] == 'Utah')) | \
        ((df_to_manip_with2['county'] == 'Carbon') & (df_to_manip_with2['state'] == 'Utah')) | \
        ((df_to_manip_with2['county'] == 'Washington') & (df_to_manip_with2['state'] == 'Utah')) | \
        (df_to_manip_with2['county'] == 'Duchesne') | \
        (df_to_manip_with2['county'] == 'Emery') | \
        ((df_to_manip_with2['county'] == 'Grand') & (df_to_manip_with2['state'] == 'Utah')) | \
        (df_to_manip_with2['county'] == 'Juab') | \
        ((df_to_manip_with2['county'] == 'Sevier') & (df_to_manip_with2['state'] == 'Utah')) | \
        (df_to_manip_with2['county'] == 'Sanpete') | \
        ((df_to_manip_with2['county'] == 'Piute') & (df_to_manip_with2['state'] == 'Utah')) | \
        ((df_to_manip_with2['county'] == 'Wayne') & (df_to_manip_with2['state'] == 'Utah')) | \
        ((df_to_manip_with2['county'] == 'Beaver') & (df_to_manip_with2['state'] == 'Utah')) | \
        (df_to_manip_with2['county'] == 'Daggett')
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
