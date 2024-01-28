import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import matplotlib.patches as mpatches
import matplotlib
import sys
import os
import numpy as np
from tueplots.constants.color import rgb
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from tueplots import bundles
from netCDF4 import Dataset
import xarray as xr
import cartopy.crs as ccrs  # plotting library for geospatial data

sys.path.insert(1, os.path.abspath(os.getcwd()))
print(os.getcwd())
print("-------------------------------------------------------")
from src.utils import download_dataset

plt.rcParams.update(bundles.icml2022())
plt.rcParams.update({"figure.dpi": 200})

# colormap for Spatial Data
alpha = 1
rb = LinearSegmentedColormap.from_list(
    "rb", [(57/255, 38/255 , 19/255, alpha), (198/255, 140/255, 83/255, alpha), 
           [1, 1, 1, alpha], (0, 0.6, 1, alpha), (0, 0, 0.8, alpha)], N=500
)

# colormap for spatial plot
rb_temp = LinearSegmentedColormap.from_list(
    "rb", [[0, 0, 153/255], [50/255, 150/255, 255/255], [1, 1, 1], [255/255, 102/255, 0], [153/255, 0, 0]], N=500
)


#######################################################
# precipitation data
#######################################################
download_dataset(file_path='precip.mon.mean.nc', 
                 url='https://downloads.psl.noaa.gov//Datasets/cmap/enh/precip.mon.mean.nc',
                 subfolder='climate_data')

data = xr.open_dataset("dat/climate_data/precip.mon.mean.nc")
df = data.to_dataframe()

# do the same for the average reference frame (1979-2000)
# data for years <1979 not available
# select data for each month of timestpan 1979-2000
dt64_start = np.datetime64('1979-01-01T00:00:00.000000000')
dt64_end = np.datetime64('2000-12-01T00:00:00.000000000')

filtered_data_2 = data.sel(time=slice(dt64_start, dt64_end))
# dataframe now contains 12 months
filtered_data_2 = filtered_data_2.mean(dim = ("time"))

# average data over whole timespan 2017-2022
start_year = '2017'
end_year = '2022'

# select data for each month of year 2017-2022
dt64_start = np.datetime64(start_year + '-01-01T00:00:00.000000000')
dt64_end = np.datetime64(end_year + '-12-01T00:00:00.000000000')

filtered_data_3 = data.sel(time=slice(dt64_start, dt64_end))
filtered_data_3 = filtered_data_3.mean(dim = ("time"))

# calculate precipitation anomaly [%] 
anomaly_2 = 100 * (filtered_data_3 - filtered_data_2) / filtered_data_2

# Create a plot
plt.rcParams.update(bundles.icml2022(column='quarter', nrows=2, ncols=1))
fig = plt.figure()

ax = fig.add_subplot(2, 1, 2, projection=ccrs.Robinson())
#ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

ax.coastlines()
plot = anomaly_2["precip"].plot(ax=ax, transform=ccrs.PlateCarree(), cmap=rb, vmin = -50, vmax = 50, add_colorbar=False)
# rename colorbar label
cb = plt.colorbar(mappable=plot, label = 'Precipitation anomalies [\%]', extend = 'both')

# add gridlines to globe
gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=False,
    linewidth=.5,
    color=rgb.tue_gray,
    alpha=0.5,
    linestyle="-",
)

gl.top_labels = False
gl.right_labels = False
ax.set_title("Mean Precipitation Anomalies: " + start_year + " - " + end_year)


#######################################################
# temperature data
#######################################################
download_dataset(file_path='NOAAGlobalTemp_v5.1.0_gridded_s185001_e202312_c20240108T150239.nc', 
                 url='https://www.ncei.noaa.gov/data/noaa-global-surface-temperature/v5.1/access/gridded/NOAAGlobalTemp_v5.1.0_gridded_s185001_e202312_c20240108T150239.nc',
                 subfolder='climate_data')

data = xr.open_dataset("dat/climate_data/NOAAGlobalTemp_v5.1.0_gridded_s185001_e202312_c20240108T150239.nc")
df = data.to_dataframe()


# average data over whole timespan 2017-2022
start_year = '2017'
end_year = '2022'
# select data for each month of timespan 2017-2022
dt64_start = np.datetime64(start_year+'-01-01T00:00:00.000000000')
dt64_end = np.datetime64(end_year+'-12-01T00:00:00.000000000')

filtered_data = data.sel(time=slice(dt64_start, dt64_end))
filtered_data = filtered_data.mean(dim = ("time"))

# Create a plot
#plt.rcParams.update(bundles.icml2022())
#fig = plt.figure()
ax = fig.add_subplot(2, 1, 1, projection=ccrs.Robinson())
#ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

ax.coastlines()
plot = filtered_data["anom"].plot(ax=ax, transform=ccrs.PlateCarree(), cmap=rb_temp, vmin=-3, vmax=3, add_colorbar=False)
# rename colorbar label
cb = plt.colorbar(mappable=plot, label = 'Annual surface temperature \n anomalies [°C]', extend = 'both')

# add gridlines to globe
gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    draw_labels=False,
    linewidth=.5,
    color=rgb.tue_gray,
    alpha=0.5,
    linestyle="-",
)

gl.top_labels = False
gl.right_labels = False
ax.set_title("Surface Temperature Anomalies: " + start_year + " - " + end_year)

plt.savefig('doc/water/fig/fig_climate/temp_precip_spatial.pdf')

plt.show()