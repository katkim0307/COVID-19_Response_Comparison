import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame


def merge_county_df_and_gdf(left_df, right_gdf):
    # Merge JHU US Counties COVID-19 Data with us_counties_gdf
    merged_df = pd.merge(
        left_df,
        right_gdf[['FULLFP', 'STATEFP', 'COUNTYFP', 'geometry', 'postcode']],
        left_on='FIPS',
        right_on='FULLFP',
        how='left',
    )

    merged_gdf = gpd.GeoDataFrame(merged_df,
                                  crs={'init': 'epsg:2163'},
                                  geometry='geometry')

    merged_gdf = merged_gdf.drop(['FULLFP'], axis=1)

    return merged_gdf
