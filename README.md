# US and South Korea COVID-19 Outbreak Response Comparison & Analysis

- **Why** are you doing this project? 
	- Amid the Novel Coronavirus pandemic, I would like to provide a clear presentation of the different COVID-19 outbreak early responses, specifically South Korea and the United States, and their outcomes
    
- **How** do you imagine you'll accomplish this project? 
	- Collect COVID-19 data of both the United States and South Korea
	- Organize and manipulate collected data
	- Create interactive maps, charts, timelines
	- Compare and analyze


## Background

The initial idea behind this project was to create a tool to automate an interactive map for **contact tracing**. Contact tracing is a concept of tracing and monitoring contacts and travels of each confirmed case (infected person).  Sharing this data anonymously to the public and notifying people of their exposure.  Ultimately this helps to prevent additional transmission.  China, South Korea, Taiwan, and Singapore effectively and successfully utilized technology for contact tracing and slowed the spread of coronavirus.  However, due to privacy concerns, western countries like the U.S., Italy, Spain, and France are experiencing difficulty deploying technology to share data on the confirmed cases. <br><br>
South Korea has been looked up to by many country leaders who are fighting against the novel coronavirus. South Korea is one of the few countries that are successfully beating the pandemic without a complete lockdown. I wanted to see how South Korea's approach and response to COVID-19 outbreak differed to the U.S.'. This will include not only COVID-19 related data (confirmed cases, fatalities, testing, etc.) but also each country administration's response including WHO/CDC/HHS's announcements and other administrative changes affected by coronavirus. I will then analyze the comparison and contrast with appropriate data visualization.


## Sample Output

#### U.S. Choropleth Map of Total Confirmed Cases
![sample01](https://raw.githubusercontent.com/katkim0307/COVID-19_Response_Comparison/master/Data/image/sample01.PNG)

#### You can view interactive choropleth maps here:
https://katkim0307.github.io/COVID-19_Response_Comparison//Data/output/us_state_latest.html
https://katkim0307.github.io/COVID-19_Response_Comparison//Data/output/us_state_history.html

#### Korea Choropleth Map of Total Confirmed Cases
![sample02](https://raw.githubusercontent.com/katkim0307/COVID-19_Response_Comparison/master/Data/image/sample02.PNG)

#### U.S. vs. Korea Early Stage of the outbreak
![sample03](https://raw.githubusercontent.com/katkim0307/COVID-19_Response_Comparison/master/Data/image/sample03.PNG)
![sample04](https://raw.githubusercontent.com/katkim0307/COVID-19_Response_Comparison/master/Data/image/sample04.PNG)
![sample05](https://raw.githubusercontent.com/katkim0307/COVID-19_Response_Comparison/master/Data/image/sample05.PNG)
![sample06](https://raw.githubusercontent.com/katkim0307/COVID-19_Response_Comparison/master/Data/image/sample06.PNG)


## Resources

#### U.S. COVID-19 Data
* Johns Hopkins University & Medicine Coronavirus Resource Center 
	- https://coronavirus.jhu.edu/map.html 
	- https://github.com/CSSEGISandData/COVID-19

* Coronavirus in New York City, The City
	- https://projects.thecity.nyc/2020_03_covid-19-tracker/

* Coronavirus in the US, New York Times 
	- https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html 
	- https://github.com/nytimes/covid-19-data
    
* Coronavirus Disease (COVID-19) - Statistics and Research, Our World in Data 
	- https://ourworldindata.org/coronavirus 
	- https://github.com/owid/covid-19-data
    
* The COVID Tracking Project 
	- https://covidtracking.com/api


#### South Korea COVID-19 Data
* Korean Centers for Disease Control and Prevention 
	- http://www.cdc.go.kr/cdc/ 
	- [Eng] https://www.cdc.go.kr/board/board.es?mid=a30402000000&bid=0030
	- [Kor] https://www.cdc.go.kr/board/board.es?mid=a20501000000&bid=0015   
    
* Korean Ministrty of Health and Welfare
	- http://ncov.mohw.go.kr/ 
    
* COVID-19 Pandemic in South Korea, Wikipedia
	- https://en.wikipedia.org/wiki/COVID-19_pandemic_in_South_Korea

* Seoul Gov
	- http://www.seoul.go.kr/coronaV/coronaStatus.do?menu_code=06


## Input Data 

#### Geodata

*  US States Boundary from the [US Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
	- https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_5m.zip
	- cb_2018_us_state_5m.shp

* US Counties Boundary from the [US Census Bureau](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html)
	- https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_5m.zip
	- cb_2018_us_county_5m.shp

* South Korea Provinces Boundary from [Natural Earth](https://www.naturalearthdata.com/downloads/)
	- https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces.zip
	- ne_10m_admin_1_states_provinces.shp


#### COVID-19 Data
* [New York Times](https://github.com/nytimes/covid-19-data) US County Time-Series Data
	- https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv

* [Johns Hopkins Uni & Med](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) for US  County Time-Series Data
	- https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv

* [the City Project](https://projects.thecity.nyc/2020_03_covid-19-tracker/) New York City Boroughs Time-Series Data 
	- https://raw.githubusercontent.com/thecityny/covid-19-nyc-data/master/borough.csv
    
* State Current Data, [COVID Tracking Project](https://covidtracking.com/api)
	- https://covidtracking.com/api/v1/states/current.json
    
* US Current Data, [COVID Tracking Project](https://covidtracking.com/api)
	- https://covidtracking.com/api/v1/us/current.json

* State Historical Data, Covid Tracking Project 
	- https://covidtracking.com/api/v1/states/daily.csv 
    
* US Historical Data, Covid Tracking Project 
	- https://covidtracking.com/api/v1/us/daily.csv 
    
* Complete COVID-19 dataset, Our World in Data
	- https://covid.ourworldindata.org/data/owid-covid-data.csv
    
* South Korea - Complete COVID-19 dataset (3 spreadsheets)
	- https://katkim0307.github.io/COVID-19_Response_Comparison/covid_19_south_korea_full_no_airport_xls.xlsx


## Technical Requirements

#### Python Libraries

* `import os`
* `import sys`
* `import request`

* `import pandas as pd` 
	- create data structures, perform data analysis and manipulation
    
* `import geopandas as gpd` / `from geopandas import GeoDataFrame`
	- work with geospatial data and perform spatial/geometric operations (done by shapely) on geometric types
	- manage projections, geocode, geoprocess
    
* `import datetime`
	- work with dates as date objects (manipulate dates)

* `import numpy as np`
	- scientific computing for multidimentional array objects

* `import matplotlib.pyplot as plt`
	- create static, animated, and interactive data visualizations

* `import matplotlib.dates as mdates`

* `import matplotlib.ticker as ticker`

* `import matplotlib.patches as patches`

* `import matplotlib.cm as cm`

* `import matplotlib.colors as colors`

* `import plotly`

* `import plotly.express as px`
	- (interface to Plotly) to create interactive choropleth maps of the US (State Level)
    
* `import plotly.figure_factory as ff`
	- (interface to Plotly) to create interactive choropleth maps of the US (County Level)

* `import plotly.graph_objs as go`
	- (interface to Plotly) to create interactive choropleth maps of the US with hover text


## Measuring Success: 

- How will you measure your project's sucess?
	- Is there some metric you'd hope to generate from your project.
    
	- Is there some plot or visualization that will be generated? 
        - There will be multiple plots and visualizations for easier understanding of input data.  I'll try to make them interactive as well.

	- Is some manual task now fully automated? 
        - COVID-19 daily data update automation


## Project Execution Plan Outline

* Background Research 
	- check location of dataset and data validity

* All Data Collection/Processing
	- Collecting and looking for additional data
	- Cleaning, organizing, formatting, modifying for data preparation

* Exploratory Spatial Data Processing for Interpretation/Analysis
	- Summarize the input data, plot and examine any columns that may be useful. 

* Exploratory Non-Spatial Data Processing for Interpretation/Analysis
	- Summarize the input data, plot and examine any columns that may be useful. 

* Results and Conclusion 
	- Key observations/findings
	- Generate Assumptions and Limitations. 

