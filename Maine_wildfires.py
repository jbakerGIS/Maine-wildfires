# Created by: Justin Baker
# Date created: Sep 2023
# Wildfire data collected from https://data-nifc.opendata.arcgis.com/
# County boundary data collected from https://public.opendatasoft.com

import geopandas as gpd
import pandas as pd
import contextily as cx
import matplotlib.pyplot as plt
from shapely.geometry import shape
from geopandas.geoseries import *

# -------------------------------- Map wildfire locations -------------------------

# Create gpd of wildfires and Maine state boundary json files
fires = gpd.read_file(
    "C:/Users/viver/OneDrive/Desktop/Portfolio/Maine/Fires.json").to_crs('EPSG:2802')

states = gpd.read_file(
    "C:/Users/viver/OneDrive/Desktop/Portfolio/Maine/gz_2010_us_040_00_500k.json"
    ).to_crs('EPSG:2802')

maine = states[states['NAME'] == 'Maine']

# Create a map showing each fortress location
ax = maine.plot(column='NAME', figsize=(9,9), alpha=0.5)
fires.plot(ax=ax, color="red", linewidths=0)
cx.add_basemap(ax, crs=fires.crs.to_string())
plt.title('Wildfire locations in Maine in 2022')
plt.axis('off')
plt.show()

# -------------------- Create an explorable map of wildfires by county ------------------------

# Create gpd of counties geojson file
counties = gpd.read_file(
    "C:/Users/viver/OneDrive/Desktop/Portfolio/Maine/Counties.geojson").to_crs('EPSG:2802')

# Subset only the name column
counties = counties[['name', 'geometry']]

# Spatial join the fires to the counties gdf
cf = gpd.sjoin(fires, counties, predicate='within')

# Calculate the number of fires in each county
numFires = cf.groupby('name').size()

# Convert the series to a DataFrame and specify column name
cf = numFires.to_frame(name='# of fires')

# Merge the dataframes
countyFires = pd.merge(counties, cf, on='name')

countyFires.plot(column='# of fires', legend=True)
plt.title('Maine Wildfires per County in 2022')
plt.axis('off')
plt.show

countyFires.explore()
