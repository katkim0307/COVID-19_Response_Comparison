import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame


def set_us_counties_boundary(input_data_filepath):
    # Read US Counties Boundary Shapefile
    us_counties_gdf = gpd.read_file('input_data_filepath')

    # Adding a 'FULLFP' column that concatenates 'STATEFP' and 'COUNTYFP'
    us_counties_gdf['FULLFP'] = us_counties_gdf['STATEFP'] + us_counties_gdf['COUNTYFP']

    # Converting the CRS to US National Atlas Equal Area Projection (EPSG: 2163)
    us_counties_gdf.to_crs(epsg=2163, inplace=True)

    # us_counties_gdf is missing the post code (stusps), therefore, merging it with fips_df
    # Read US State Name, FIPS, and Postcode csv file
    fips_csv_dir = 'Data/input/us_state_fips/us-state-ansi-fips.csv'
    fips_df = pd.read_csv(fips_csv_dir, dtype={' fips': object})

    # Rename columns
    fips_df.rename(columns=
                   {' fips': 'fips',
                    ' stusps': 'postcode', },
                   inplace=True)

    # Attribute Joins - Merging `us_counties_gdf` and `fips_df` on `'STATEFP'` and `'fips'`
    merged_df = pd.merge(
        left=us_counties_gdf,
        right=fips_df,
        how='left',
        left_on='STATEFP',
        right_on='fips'
    )

    # Remove (drop) 'fips' column
    merged_df = merged_df.drop(['fips'], axis=1)

    # Make us_gdf a GeoDataFrame of merged_df
    us_counties_gdf = gpd.GeoDataFrame(merged_df,
                                       crs={'init': 'epsg:2163'},
                                       geometry=merged_df['geometry'])

    return us_counties_gdf
