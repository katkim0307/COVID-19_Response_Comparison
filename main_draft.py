import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)


import pandas as pd
import geopandas as gpd
import pyproj
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.colors as colors
import plotly
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff


%matplotlib inline


from Tools.us_states_gdf import set_us_states_boundary
from Tools.us_counties_gdf import set_us_counties_boundary
from Tools.kor_provinces_gdf import set_kor_provinces_boundary

from Tools.jhu_county_df_manipulate import manipulate_jhu_county_df
from Tools.ctp_states_now_df import set_ctp_states_now_df
from Tools.ctp_us_hist_df import set_ctp_us_hist_df
from Tools.ctp_states_hist_df import set_ctp_states_hist_df
from Tools.merge_state_dfgdf import merge_state_df_and_gdf
from Tools.merge_county_dfgdf import merge_county_df_and_gdf
from Tools.kor_df import set_kor_df
from Tools.merge_province_dfgdf import merge_province_df_and_gdf

############################################
##                                        ##
##      All Boundary GeoDataFrames        ##
##                                        ##
############################################

# US States Boundary
us_states_gdf = set_us_states_boundary('Data/input/us_state/cb_2018_us_state_5m.shp')

# US Counties Boundary
us_counties_gdf = set_us_counties_boundary('Data/input/us_counties/cb_2018_us_county_5m.shp')

# KOR Provinces/Cities Boundary
kor_provinces_gdf = set_kor_provinces_boundary(
    'Data/input/ne_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp')

############################################
##                                        ##
##        All COVID-19 DataFrames         ##
##                                        ##
############################################

# NYTimes US County COVID-19 Data
nytimes_counties_df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
nytimes_counties_df['datetime'] = pd.to_datetime(nytimes_counties_df['date'])

# JHU US County COVID-19 Data
jhu_county_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
                            '/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
jhu_county_df.drop(['UID', 'iso2', 'iso3', 'code3', 'Country_Region', 'Combined_Key'], axis=1, inplace=True)
jhu_county_df = manipulate_jhu_county_df(jhu_county_df, nytimes_counties_df)

# COVID Tracking Project: US COVID-19 Current Data
ctp_us_now_df = pd.read_json('https://covidtracking.com/api/v1/us/current.json')[['positive', 'death', 'total']]

# COVID Tracking Project: US State COVID-19 Current Data
ctp_states_now_df = set_ctp_states_now_df('https://covidtracking.com/api/v1/states/current.json')

# COVID Tracking Project: US COVID-19 History Data
ctp_us_hist_df = set_ctp_us_hist_df('https://covidtracking.com/api/v1/us/daily.json')

# Creating a DataFrame for plotting charts with date as the index (Set 'datetime' as the index)
ctp_us_hist_plot_df = ctp_us_hist_df[['datetime', 'date', 'positive', 'death', 'test']].copy()
ctp_us_hist_plot_df.set_index('datetime', inplace=True)

# COVID Tracking Project: US States COVID-19 History Data
ctp_states_hist_df = set_ctp_states_hist_df('https://covidtracking.com/api/v1/states/daily.json')

# Creating a DataFrame for plotting charts with date as the index (Set 'datetime' as the index)
ctp_states_hist_plot_df = ctp_states_hist_df[['datetime', 'date', 'state', 'fips', 'positive', 'death', 'test']].copy()
ctp_states_hist_plot_df.set_index('datetime', inplace=True)

# KOR Province COVID-19 Current Data
kor_province_now_df = pd.read_excel('Data/input/covid_19_south_korea_full_no_airport_xls.xlsx',
                                    sheet_name='covid_19_update')
kor_province_now_df.fillna(0, inplace=True)

# KOR COVID-19 History Data
kor_hist_df = set_kor_df('Data/input/covid_19_south_korea_full_no_airport_xls.xlsx', 'covid_19_daily_country')

# Creating a DataFrame for plotting charts (Set 'datetime' as the index)
kor_hist_plot_df = kor_hist_df[['datetime', 'Date', 'Confirm_New', 'Confirm_Tot', 'Death_New', 'Death_Tot',
                                'Test_New', 'Test_Tot', 'Test_Curr']].copy()
kor_hist_plot_df.set_index('datetime', inplace=True)

# KOR Province COVID-19 History Data
kor_province_hist_df = set_kor_df('Data/input/covid_19_south_korea_full_no_airport_xls.xlsx', 'covid_19_daily_province')

# Creating a DataFrame for plotting charts (Set 'datetime' as the index)
kor_province_hist_plot_df = kor_province_hist_df[['datetime', 'Date', 'Province', 'Confirm_New', 'Confirm_Tot',
                                                  'Death_New', 'Death_Tot', 'Test_New', 'Test_Tot', 'Test_Curr']].copy()
kor_province_hist_plot_df.set_index('datetime', inplace=True)

############################################
##                                        ##
##       All Merged GeoDataFrames         ##
##                                        ##
############################################

# Merge ctp_states_now_df with us_states_gdf
us_cov19_states_now_gdf = merge_state_df_and_gdf(ctp_states_now_df, us_states_gdf)
us_cov19_states_gdf = merge_state_df_and_gdf(ctp_states_hist_df, us_states_gdf)

# Creating a GeoDataFrame for plotting charts with date as the index (Set 'datetime' as the index)
us_cov19_states_plot_gdf = us_cov19_states_gdf[
    ['datetime', 'date', 'NAME', 'state', 'fips', 'positive', 'death', 'test', 'coords', 'geometry']].copy()
us_cov19_states_plot_gdf.set_index('datetime', inplace=True)

# Merge jhu_county_df with us_counties_gdf
us_cov19_counties_gdf = merge_county_df_and_gdf(jhu_county_df, us_counties_gdf)

# Merge kor_province_now_df with kor_provinces_gdf
kor_cov19_province_now_gdf = merge_province_df_and_gdf(kor_province_now_df, kor_provinces_gdf)

# Merge kor_province_hist_df with kor_provinces_gdf
kor_cov19_province_hist_gdf = merge_province_df_and_gdf(kor_province_hist_df, kor_provinces_gdf)

# Creating a GeoDataFrame for plotting charts (Set 'datetime' as the index)
kor_cov19_province_hist_plot_gdf = kor_cov19_province_hist_gdf.copy()
kor_cov19_province_hist_plot_gdf.set_index('datetime', inplace=True)

############################################
##                                        ##
##          Data Visualizations           ##
##                                        ##
############################################

#------------------------------------------------------#
# Latest US State Confirmed Cases Basic Choropleth Map #
#------------------------------------------------------#
fig, ax = plt.subplots(figsize=(12, 15))

us_cov19_states_now_gdf.plot(
    ax=ax,
    column='positive',
    cmap='Reds',
    edgecolor='white',
    legend=True,
    scheme='BoxPlot',
    legend_kwds={'loc': 'lower left'},
)

# Title
today_date = datetime.datetime.now()
ax.set_title('US Total Confirmed Cases (as of ' + today_date.strftime('%b %d') + ')', fontdict={'size': 20});

# Normalize the Legend Color and create the legend bar
vmin, vmax = us_cov19_states_now_gdf.positive.min(), us_cov19_states_now_gdf.positive.max()
legend_bar = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap='Reds')

# Add the Color Legend Bar
fig.colorbar(legend_bar, ax=ax, orientation='horizontal', fraction=0.05, pad=0.05, shrink=0.6)

# Displaying each State Postcode
for idx, row in us_cov19_states_now_gdf.iterrows():
    plt.annotate(s=row['state'], xy=row['coords'],
                 horizontalalignment='center',
                 color='lightgrey',
                 )

# Turn off the box and the axes label
ax.axis(False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

# Crop the map to an appropriate size (via coordinate)
ax.set_ylim(-2500000, 1000000);

#----------------------------------------------------------#
# Latest KOR Province Confirmed Cases Basic Choropleth Map #
#----------------------------------------------------------#
fig, ax = plt.subplots(figsize=(10,15))

# Plot
kor_cov19_province_now_gdf.plot(
    ax=ax,
    column='Confirm_Tot',
    cmap='Reds',
    edgecolor='lightgrey',
    legend=True,
    scheme='percentiles', # or boxplot,
    legend_kwds={'loc': 'lower right'},
)

# Title
kor_update = kor_province_now_df.iloc[-1]['Date'].to_pydatetime()
ax.set_title('South Korea Total Confirmed Cases (as of ' + kor_update.strftime('%b %d') + ')', fontdict={'size':20});

# Normalize the Legend Color and create the legend bar
vmin, vmax = kor_cov19_province_now_gdf.Confirm_Tot.min(), kor_cov19_province_hist_plot_gdf.Confirm_Tot.max()
legend_bar = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap='Reds')

# Add the Color Legend Bar
fig.colorbar(legend_bar, ax=ax, orientation='horizontal', fraction=0.05, pad=0.04, shrink=0.6)

# Displaying each State Postcode
for idx, row in kor_cov19_province_now_gdf.iterrows():
    plt.annotate(s=row['Province'], xy=row['coords'],
                 horizontalalignment='center',
                 color='#7F8C8D',
                )

# Turn off the box and the axes label
ax.axis(False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

#----------------------------------------------------------------#
# History of US State Confirmed Cases Time-series Choropleth Map #
#----------------------------------------------------------------#
ctp_states_hist_df = ctp_states_hist_df.sort_values(by=['date'])

color_scale = ['#ffffff', '#ffe6e6', '#ffcccc', '#ff9999', '#ff6666', '#ff3333',
               '#ff0000', '#e60000', '#cc0000', '#b30000', '#990000', '#800000']

fig = px.choropleth(
    ctp_states_hist_df,
    color='positive',
    locations='state',
    locationmode = 'USA-states',
    scope='usa',
    hover_name='state',
    hover_data=['test', 'death'],
    animation_frame='date',
    title="Daily New COVID-19 Confirmed Cases",
    color_continuous_scale= color_scale, # 'YlOrRd',
)

# create a slider for date that can be manually toggled.
fig['layout'].pop('updatemenus')

fig.show()




