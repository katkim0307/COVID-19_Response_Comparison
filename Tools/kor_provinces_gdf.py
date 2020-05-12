import geopandas as gpd


def set_kor_provinces_boundary(input_data_filepath):
    # Read in Natural Earth Large Scale Cultural Data (Admin 1 - States and Provinces) Boundary Shapefile
    ne_admin_1_states_gdf = gpd.read_file(input_data_filepath)

    # Create a GeoDataFrame for South Korea Provinces & Special/Metropolitan Cities ONLY
    south_korea_gdf = ne_admin_1_states_gdf[ne_admin_1_states_gdf['admin'] == 'South Korea']

    # Keep the only columns that needed
    south_korea_gdf = south_korea_gdf[
        ['geonunit', 'gu_a3', 'gn_name', 'name_de', 'fips', 'latitude', 'longitude', 'geometry']]

    # Adding a column 'coords' for later use (labeling each Province)
    south_korea_gdf['coords'] = south_korea_gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    south_korea_gdf['coords'] = [coords[0] for coords in south_korea_gdf['coords']]

    return south_korea_gdf
