import numpy as np
import os

# read header
file_name = os.path.relpath('datasets/gmia_v5_aei_pct.asc')
header_rows = 6 # six rows for header information
header = {} # store header information including ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value
row_ite = 1
with open(file_name, 'rt') as file_h:
     for line in file_h:
        if row_ite <= header_rows:
             line = line.split(" ", 1)
             header[line[0]] = float(line[1])
        else:
             break
        row_ite = row_ite+1
# read data array
data_array = np.loadtxt(file_name, skiprows=header_rows, dtype='float64')

left = header['xllcorner']
right = header['xllcorner']+header['ncols']*header['cellsize']
bottom = header['yllcorner']
top = header['yllcorner']+header['nrows']*header['cellsize']
map_extent = (left, right, bottom, top)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
img = plt.imshow(data_array, extent=map_extent)

plt.show()

from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes(loc='right', size='3%', pad=0.05,)
cbar = plt.colorbar(img, cax=cax)