import pandas as pd
import geopandas as gpd


def merge_province_df_and_gdf(left_df, right_gdf):
    merged_df = pd.merge(
        left_df,
        right_gdf[['geonunit', 'name_de', 'fips', 'latitude', 'longitude', 'geometry', 'coords']],
        left_on='Province',
        right_on='name_de',
        how='left',
    )

    merged_df = merged_df.drop(['name_de'], axis=1)

    merged_gdf = gpd.GeoDataFrame(merged_df,
                                  crs={'init': 'epsg:4326'},
                                  geometry='geometry')

    return merged_gdf

