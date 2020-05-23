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

from Tools.us_states_gdf import set_us_states_boundary
from Tools.us_counties_gdf import set_us_counties_boundary
from Tools.kor_provinces_gdf import set_kor_provinces_boundary

from Tools.jhu_county_df_manipulate import manipulate_jhu_county_df
from Tools.ctp_states_now_df import set_ctp_states_now_df
from Tools.ctp_us_hist_df import set_ctp_us_hist_df
from Tools.ctp_states_hist_df import set_ctp_states_hist_df
from Tools.merge_state_dfgdf import merge_state_df_and_gdf
from Tools.merge_county_dfgdf import merge_county_df_and_gdf
from Tools.convert_to_gdf import convert_to_gdf
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

# Our World in Data (owid) COVID-19 Data
fields = ['iso_code', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
          'total_cases_per_million', 'new_cases_per_million', 'total_deaths_per_million', 'new_deaths_per_million',
          'total_tests', 'new_tests', 'total_tests_per_thousand', 'new_tests_per_thousand', 'population']
owid_complete_df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv', usecols=fields)
owid_complete_df = owid_complete_df[
    (owid_complete_df['location'] == 'United States') |
    (owid_complete_df['location'] == 'South Korea')
    ]

owid_complete_df['datetime'] = pd.to_datetime(owid_complete_df['date'])

# US OWID Data
owid_us_df = owid_complete_df[owid_complete_df['iso_code'] == 'USA']
owid_us_df['datetime'] = pd.to_datetime(owid_us_df['date'])
owid_us_plot_df = owid_us_df.copy()
owid_us_plot_df.set_index('datetime', inplace=True)

# KOR OWID Data
owid_kor_df = owid_complete_df[owid_complete_df['iso_code'] == 'KOR']
owid_kor_df['datetime'] = pd.to_datetime(owid_kor_df['date'])
owid_kor_plot_df = owid_kor_df.copy()
owid_kor_plot_df.set_index('datetime', inplace=True)

# NYTimes US County COVID-19 Data
nytimes_counties_df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
nytimes_counties_df['datetime'] = pd.to_datetime(nytimes_counties_df['date'])

# TheCity (NYC) Boroughs COVID-19 Data
thecity_df = pd.read_csv('https://raw.githubusercontent.com/thecityny/covid-19-nyc-data/master/borough.csv')

# JHU US County COVID-19 Data
jhu_county_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
                            '/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
jhu_county_df.drop(['UID', 'iso2', 'iso3', 'code3', 'Country_Region', 'Combined_Key'], axis=1, inplace=True)
jhu_county_df = manipulate_jhu_county_df(jhu_county_df, thecity_df, nytimes_counties_df)

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
us_cov19_states_now_df = merge_state_df_and_gdf(ctp_states_now_df, us_states_gdf)
us_cov19_states_now_gdf = convert_to_gdf(us_cov19_states_now_df)
us_cov19_states_df = merge_state_df_and_gdf(ctp_states_hist_df, us_states_gdf)
us_cov19_states_gdf = convert_to_gdf(us_cov19_states_df)

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

# ----------------------------------------------------------#
# Latest KOR Province Confirmed Cases Basic Choropleth Map  #
# ----------------------------------------------------------#
fig, ax = plt.subplots(figsize=(10, 15))

# Plot
kor_cov19_province_now_gdf.plot(
    ax=ax,
    column='Confirm_Tot',
    cmap='Reds',
    edgecolor='lightgrey',
    legend=True,
    scheme='boxplot',
    legend_kwds={'loc': 'lower right'},
)

# Title
kor_update = kor_province_now_df.iloc[-1]['Date'].to_pydatetime()
ax.set_title('South Korea Total Confirmed Cases (as of ' + kor_update.strftime('%b %d') + ')', fontdict={'size': 20})

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

# ------------------------------------------------------#
# Latest US State Confirmed Cases Basic Choropleth Map  #
# ------------------------------------------------------#
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
ax.set_title('US Total Confirmed Cases (as of ' + today_date.strftime('%b %d') + ')', fontdict={'size': 20})

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
ax.set_ylim(-2500000, 1000000)

# ------------------------------------------------------------#
# Latest US State Confirmed Cases Interactive Choropleth Map  #
# ------------------------------------------------------------#
# color scheme for the map plot (white to red)
color_scale = ['#ffffff', '#ffe6e6', '#ffcccc', '#ffb3b3', '#ff9999', '#ff8080', '#ff6666', '#ff4d4d', '#ff3333',
               '#ff1a1a', '#ff0000', '#e60000', '#cc0000', '#b30000', '#990000', '#800000', '#660000', '#4d0000']

# creating a new column that will include the mouse-hovering text for each state
for col in us_cov19_states_now_df.columns:
    us_cov19_states_now_df[col] = us_cov19_states_now_df[col].astype(str)

us_cov19_states_now_df['text'] = us_cov19_states_now_df['NAME'] + '<br>' + \
                                 'Deaths: ' + us_cov19_states_now_df['death'] + '<br>' + \
                                 'Tests: ' + us_cov19_states_now_df['test']

us_cov19_states_now_df[['positive', 'death', 'test']] = us_cov19_states_now_df[['positive', 'death', 'test']].apply(
    pd.to_numeric)

zmax = us_cov19_states_now_df['positive'].max()
zmid = us_cov19_states_now_df['positive'].median()
zmin = us_cov19_states_now_df['positive'].min()

fig = go.Figure(data=go.Choropleth(
    locations=us_cov19_states_now_df['state'],  # for county -> FIPS, for State -> post code, for Country -> ISO Code
    z=us_cov19_states_now_df['positive'],  # the column to color-code
    locationmode='USA-states',
    zmax=zmax, zmid=zmid, zmin=zmin,
    colorscale=color_scale,
    autocolorscale=False,
    text=us_cov19_states_now_df['text'],  # hover text
    marker_line_color='white',  # for the lines separating states
    marker_line_width=2,
    colorbar_title='Confirmed Cases'
))

# updating the layout
fig.update_layout(
    title_text='US State COVID-19 Confirmed Cases (latest update: ' + today_date.strftime('%b %d') + ')',
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa'),
    )
)

fig.show()

# ----------------------------------------------------#
# US State Confirmed Cases Time-series Choropleth Map #
# ----------------------------------------------------#
ctp_states_hist_df = ctp_states_hist_df.sort_values(by=['date'])

color_scale = ['#ffffff', '#ffe6e6', '#ffcccc', '#ffb3b3', '#ff9999', '#ff8080', '#ff6666', '#ff4d4d', '#ff3333',
               '#ff1a1a', '#ff0000', '#e60000', '#cc0000', '#b30000', '#990000', '#800000', '#660000', '#4d0000']

fig = px.choropleth(
    ctp_states_hist_df,
    color='positive',
    locations='state',
    locationmode='USA-states',
    scope='usa',
    hover_name='state',
    hover_data=['test', 'death'],
    animation_frame='date',
    title="Daily New COVID-19 Confirmed Cases",
    color_continuous_scale=color_scale,
)

# create a slider for date that can be manually toggled.
fig['layout'].pop('updatemenus')

fig.show()

# -----------------------------------------#
# US County Confirmed Cases Choropleth Map #
# -----------------------------------------#
# Declaring a DataFrame that copies rows from another jhu_county_df3 that has the latest date attribute
jhu_county_latest_df = (jhu_county_df[jhu_county_df['datetime'] == jhu_county_df.iloc[-1]['datetime']])

color_scale = ['#ffffff', '#ffe6e6', '#ffcccc', '#ffb3b3', '#ff9999', '#ff8080', '#ff6666', '#ff4d4d', '#ff3333',
               '#ff1a1a', '#ff0000', '#e60000', '#cc0000', '#b30000', '#990000', '#800000', '#660000', '#4d0000']

quantiles = list(jhu_county_latest_df['Cases'].quantile(
    [0.1, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]))
fips = jhu_county_latest_df['FIPS'].tolist()
values = jhu_county_latest_df['Cases'].tolist()

fig = ff.create_choropleth(
    fips=fips, values=values,
    scope=['usa'],
    binning_endpoints=quantiles,
    colorscale=color_scale,
    show_state_data=False,
    show_hover=True,
    county_outline=dict(color='white', width=0.25),
    asp=2.9,
    title_text='US State COVID-19 Confirmed Cases (latest update: ' + today_date.strftime('%b %d') + ')',
    legend_title='confirmed cases'
)

fig.layout.template = None

fig.show()

# -------------------------------------------#
#                 US vs. KOR                 #
# Overlaid Line Graph of Total Cases & Tests #
# -------------------------------------------#
fig, ax = plt.subplots(figsize=(10, 6))
ax2 = ax.twinx()

ctp_us_hist_plot_df.plot(
    ax=ax,
    y=['positive', 'test'],
    color=['#F1948A', '#82E0AA'],
    linewidth=3,
    ylim=(0, 1000000),
)

kor_hist_plot_df.plot(
    ax=ax2,
    ls='--',
    y=['Confirm_Tot', 'Test_Tot'],
    color=['#F1948A', '#82E0AA'],
    linewidth=3,
    ylim=(0, 1000000),
)

ax.legend(['US Total Confirmed', 'US Total Tests'], loc='upper left')
ax2.legend(['KOR Total Confirmed', 'KOR Total Tests'], loc=(0.01, 0.72))

ax2.get_yaxis().set_visible(False)

ax.grid(linewidth=0.2)

ax2.xaxis.set_major_locator(mdates.WeekdayLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.set_title('US Vs. South Korea \n COVID-19 Total Cases & Tests', fontdict={'size': 20})

plt.show()

# ------------------------------------------------------------------------------#
#                                  US vs. KOR                                   #
# Line Graph Comparison of Total Cases per million and Total Tests per thousand #
# ------------------------------------------------------------------------------#

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

ax1.plot(owid_us_plot_df['total_cases_per_million'], label='US Cases per mill', color='#F1948A', linewidth=3)
ax1.plot(owid_kor_plot_df['total_cases_per_million'], label='KOR Cases per mill', color='#F1948A', linewidth=3, ls='--')

ax2.plot(owid_us_plot_df['total_tests_per_thousand'], label='US Tests per 1000', color='#82E0AA', linewidth=3)
ax2.plot(owid_kor_plot_df['total_tests_per_thousand'], label='KOR Tests per 1000', color='#82E0AA', linewidth=3,
         ls='--')

# Set titles
ax1.set_title('US vs. KOR Total Cases per million', fontdict={'size': 20})
ax2.set_title('US vs. KOR Total Tests per thousand', fontdict={'size': 20})

# Set legends
ax1.legend(['US Cases per million', 'KOR Cases per million'], loc='upper left')
ax2.legend(['US Tests per thosand', 'KOR Tests per thousand'], loc='upper left')

# Set axes limit
start_date = datetime.datetime(2020, 1, 20)
end_date = today_date  # datetime.datetime(2020, 4, 30)
ax1.set_xlim(start_date, end_date)
ax2.set_xlim(start_date, end_date)
ax1.set_ylim(0, 1000)
ax2.set_ylim(0, 50)

# Set grid lines
ax1.grid(linewidth=0.2)
ax2.grid(linewidth=0.2)

# set ticks every week
ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# #set major ticks format
ax2.xaxis.set_major_locator(mdates.WeekdayLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# --------------------------------------------------#
#                 Early US vs. KOR                  #
# Line Graph Comparison of Total Cases/Deaths/Tests #
# --------------------------------------------------#
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

ax1.plot(ctp_us_hist_plot_df['test'], label='US Tests', color='#82E0AA', linewidth=3)
ax1.plot(ctp_us_hist_plot_df['positive'], label='US Cases', color='#FAD7A0', linewidth=3)
ax1.plot(ctp_us_hist_plot_df['death'], label='US Deaths', color='#F1948A', linewidth=3)

ax2.plot(kor_hist_plot_df['Test_Tot'], label='KOR Tests', color='#82E0AA', linewidth=3)
ax2.plot(kor_hist_plot_df['Confirm_Tot'], label='KOR Cases', color='#FAD7A0', linewidth=3)
ax2.plot(kor_hist_plot_df['Death_Tot'], label='KOR Deaths', color='#F1948A', linewidth=3)

# Set titles
ax1.set_title('Early US COVID-19 Total Cases/Deaths/Tests', fontdict={'size': 20})
ax2.set_title('Early KOR COVID-19 Total Cases/Deaths/Tests', fontdict={'size': 20})

# Set legends
ax1.legend(['US Total Test', 'US Total Confirmed', 'US Total Death'], loc='upper left')
ax2.legend(['KOR Total Test', 'KOR Total Confirmed', 'KOR Total Death'], loc='upper left')

# Set axes limit
start_date = datetime.datetime(2020, 1, 20)
end_date = datetime.datetime(2020, 3, 31)
ax1.set_xlim(start_date, end_date)
ax2.set_xlim(start_date, end_date)
ax1.set_ylim(0, 70000)
ax2.set_ylim(0, 70000)

# Set grid lines
ax1.grid(linewidth=0.2)
ax2.grid(linewidth=0.2)

# set ticks every week
ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# set major ticks format
ax2.xaxis.set_major_locator(mdates.WeekdayLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# ----------------------------------------#
#            Early US vs. KOR             #
# Bar & Line Graph of Total Cases & Tests #
# ----------------------------------------#
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

ax1.bar(ctp_us_hist_plot_df.index,
        ctp_us_hist_plot_df['test'],
        alpha=0.5,
        label='US Test',
        color='#B2BABB', )

ax1.plot(ctp_us_hist_plot_df['positive'],
         label='US Cases',
         color='#F1948A',
         linewidth=3,
         )

ax2.bar(kor_hist_plot_df.index,
        kor_hist_plot_df['Test_Tot'],
        alpha=0.5,
        label='KOR Test',
        color='#B2BABB', )

ax2.plot(kor_hist_plot_df['Confirm_Tot'],
         label='KOR Cases',
         color='#F1948A',
         linewidth=3,
         )

# Set titles
ax1.set_title('Early US Total Cases & Tests', fontdict={'size': 20})
ax2.set_title('Early KOR Total Cases & Tests', fontdict={'size': 20})

# Set legends
ax1.legend(['US Tests', 'US Cases'], loc='upper left')
ax2.legend(['KOR Tests', 'KOR Cases'], loc='upper left')

# Set axes limit
start_date = datetime.datetime(2020, 1, 20)
end_date = datetime.datetime(2020, 3, 31)
ax1.set_xlim(start_date, end_date)
ax2.set_xlim(start_date, end_date)
ax1.set_ylim(0, 700000)
ax2.set_ylim(0, 700000)

# set ticks every week
ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# set major ticks format
ax2.xaxis.set_major_locator(mdates.WeekdayLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

# -------------------------------------------------#
#                Early US vs. KOR                  #
# Overlaid Bar & Line Graph of Total Cases & Tests #
# -------------------------------------------------#
fig, ax = plt.subplots(figsize=(15, 6))

ax.bar(ctp_us_hist_plot_df.index,
       ctp_us_hist_plot_df['test'],
       alpha=0.5, label='US Test',
       color='#82E0AA',
       )

ax.bar(kor_hist_plot_df.index,
       kor_hist_plot_df['Test_Tot'],
       alpha=0.5,
       label='KOR Test',
       color='#B2BABB',
       )

ax.plot(
    ctp_us_hist_plot_df['positive'],
    label='US Cases',
    color='#F1948A',
    linewidth=3,
)

ax.plot(
    kor_hist_plot_df['Confirm_Tot'],
    label='KOR Cases',
    ls='--',
    color='#F1948A',
    linewidth=3,
)

# set the range of axes
start_date = datetime.datetime(2020, 1, 20)
end_date = datetime.datetime(2020, 3, 31)
ax.set_xlim(start_date, end_date)
ax.set_ylim(0, 700000)

# set the legend location
ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

# set ticks every week
ax.xaxis.set_major_locator(mdates.WeekdayLocator())
# set major ticks format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

plt.title('US Vs. South Korea \n COVID-19 Total Cases & Tests \n (Jan 20 - Mar 31)',
          fontdict={'size': 20})
