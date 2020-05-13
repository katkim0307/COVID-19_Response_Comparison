import pandas as pd


def merge_state_df_and_gdf(left_df, right_gdf):
    merged_df = pd.merge(
        left_df,
        right_gdf[['STATEFP', 'NAME', 'coords', 'geometry']],
        left_on='fips',
        right_on='STATEFP',
        how='left',
    )

    return merged_df
