import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame


def merge_state_df_and_gdf(left_df, right_gdf):
    merged_df = pd.merge(
        left_df,
        right_gdf[['STATEFP', 'NAME', 'coords', 'geometry']],
        left_on='fips',
        right_on='STATEFP',
        how='left',
    )

    merged_gdf = gpd.GeoDataFrame(merged_df,
                                  crs={'init': 'epsg:2163'},
                                  geometry='geometry')

    merged_gdf = merged_gdf.drop(['STATEFP'], axis=1)

    return merged_gdf
