import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame


def convert_to_gdf(df):
    converted_gdf = gpd.GeoDataFrame(df,
                                     crs={'init': 'epsg:2163'},
                                     geometry='geometry')

    converted_gdf = converted_gdf.drop(['STATEFP'], axis=1)

    return converted_gdf
