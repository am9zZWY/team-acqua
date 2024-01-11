import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

from src.utils import open_dataset, save_fig, to_dat_path

FIG_PATH = 'fig_irrigated_area_map'
FIG_NAME = 'fig_irrigated_area_map.pdf'
CSV_PATH = 'gmia_v5_aei_pct.asc'

# TODO: add comments to explain the code

# read header
header_rows = 6  # six rows for header information
header = {}  # store header information including ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value
row_ite = 1
with open_dataset(CSV_PATH, 'rt') as file_h:
    for line in file_h:
        if row_ite <= header_rows:
            line = line.split(" ", 1)
            header[line[0]] = float(line[1])
        else:
            break
        row_ite = row_ite + 1
# read data array
data_array = np.loadtxt(to_dat_path(CSV_PATH), skiprows=header_rows, dtype='float64')

left = header['xllcorner']
right = header['xllcorner'] + header['ncols'] * header['cellsize']
bottom = header['yllcorner']
top = header['yllcorner'] + header['nrows'] * header['cellsize']
map_extent = (left, right, bottom, top)

fig, ax = plt.subplots(1)
img = plt.imshow(data_array, extent=map_extent)

plt.show()

divider = make_axes_locatable(ax)
cax = divider.append_axes(size='3%', pad=0.05, position='right')
cbar = plt.colorbar(img, cax=cax)

# Save the figure
save_fig(fig, fig_name='fig_irrigated_area_map', fig_path=FIG_PATH)
