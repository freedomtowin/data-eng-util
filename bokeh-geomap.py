# Import geopandas package
import geopandas as gpd
# Read in shapefile and examine data
# https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
shp_df_cnty = gpd.read_file('data/cb_2019_us_county_500k/cb_2019_us_county_500k.shp')
shp_df_zip = gpd.read_file('data/cb_2019_us_zcta510_500k/cb_2019_us_zcta510_500k.shp')
shp_df_st = gpd.read_file('data/cb_2019_us_state_500k/cb_2019_us_state_500k.shp')
shp_df_pl = gpd.read_file('data/cb_2019_us_place_500k/cb_2019_us_place_500k.shp')
shp_df_tr = gpd.read_file('data/cb_2019_us_tract_500k/cb_2019_us_tract_500k.shp')

shp_df_st.head()

shp_df_st = shp_df_st[['STATEFP','STUSPS']].rename(columns={'STUSPS':'ST_NAME'})
shp_df_cnty = shp_df_cnty.merge(shp_df_st, on='STATEFP')
shp_df_tr = shp_df_tr.merge(shp_df_st, on='STATEFP')

shp_df_cnty = shp_df_cnty.loc[~shp_df_cnty['ST_NAME'].isin(['AK', 'HI','PR'])]
shp_df_tr = shp_df_tr.loc[~shp_df_tr['ST_NAME'].isin(['AK', 'HI','PR'])]

import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider)
from bokeh.layouts import column, row, widgetbox
from bokeh.palettes import brewer
from bokeh.plotting import figure
from bokeh.io import output_notebook
# Input GeoJSON source that contains features for plotting
geosource = GeoJSONDataSource(geojson = shp_df_cnty.to_json())

output_notebook()

# Define color palettes
palette = brewer['BuGn'][8]
palette = palette[::-1] # reverse order of colors so higher values have darker colors
# Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40000000)

color_bar = ColorBar(color_mapper = color_mapper, 
                     label_standoff = 8,
                     width = 500, height = 20,
                     border_line_color = None,
                     location = (0,0), 
                     orientation = 'horizontal',
#                      major_label_overrides = tick_labels
                    )

# Create figure object.
p = figure(title = 'Water Area by County', 
           plot_height = 600 ,
           plot_width = 950, 
           toolbar_location = 'below',
           tools = "pan, wheel_zoom, box_zoom, reset",
           x_range=(-130, -65), y_range=(20, 55))



p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
# Add patch renderer to figure.
states = p.patches('xs','ys', source = geosource,
#                    fill_color = None,
                   fill_color = {'field' :'AWATER','transform':color_mapper},
                   line_color = "gray", 
                   line_width = 0.25, 
                   fill_alpha = 1)
# Create hover tool
p.add_tools(HoverTool(renderers = [states],
                      tooltips = [('State','@NAME'),
                                ('Population','@AWATER')]))

p.add_layout(color_bar, 'below')

show(p)


#check to see which census tract a location is in
from shapely.geometry import Point, Polygon
lat,long = -80,40

pnt = Point(lat, long)

for i in shp_df_tr.index:
    if pnt.within(shp_df_tr.loc[i,'geometry'])==True:
        print(shp_df_tr.loc[i,'TRACTCE'])
