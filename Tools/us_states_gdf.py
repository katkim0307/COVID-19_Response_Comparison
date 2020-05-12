import geopandas as gpd


def set_us_states_boundary(input_data_filepath):
    # Read US States Boundary Shapefile
    us_states_gdf = gpd.read_file(input_data_filepath)

    # Converting the CRS to US National Atlas Equal Area Projection (EPSG: 2163)
    us_states_gdf.to_crs(epsg=2163, inplace=True)

    # Adding a column 'coords' for later use (labeling each State)
    us_states_gdf['coords'] = us_states_gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    us_states_gdf['coords'] = [coords[0] for coords in us_states_gdf['coords']]

    # There are US States/Territories that I don't want to include for data mapping purposes.
    # Palau (PW/70), Guam (GU/66), Northern Mariana Islands (MP/69), American Samoa (AS/60),
    # Hawaii (HI/15), Puerto Rico (PR/72), and Virgin Islnads (VI/78).
    us_states_gdf = us_states_gdf[
        (us_states_gdf['STATEFP'] != '70') &
        (us_states_gdf['STATEFP'] != '66') &
        (us_states_gdf['STATEFP'] != '69') &
        (us_states_gdf['STATEFP'] != '60') &
        (us_states_gdf['STATEFP'] != '15') &
        (us_states_gdf['STATEFP'] != '72') &
        (us_states_gdf['STATEFP'] != '78')
    ]

    return us_states_gdf
