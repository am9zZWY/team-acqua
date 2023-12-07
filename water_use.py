import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib
import numpy as np
from tueplots.constants.color import rgb



target_year = 1990

'''import csv'''
import requests
import os.path

CSV_URL = 'https://yaon.org/data.csv'
FILE_NAME = 'fao_aquastat.csv'

if not os.path.isfile(FILE_NAME):
    print(f'Downloading {FILE_NAME}')
    r = requests.get(CSV_URL)
    with open(FILE_NAME, 'wb') as f:
        f.write(r.content)
else:
    print(f'{FILE_NAME} already exists')

import_df = pd.read_csv(FILE_NAME)
import_df.drop(columns=['Unnamed: 0'], inplace=True)
'''Format dataframe'''
df = import_df.pivot_table(index=['Country', 'Year'], columns='Variable', values='Value', aggfunc='first')
df.reset_index(inplace=True)

df.head()



#three types of water withdrawal: agricultural, industrial and municipial water withdrawal

'''relevant variables for us'''
relevant_vars = ['Total water withdrawal', 'Municipal water withdrawal', 'Industrial water withdrawal', 'Agricultural water withdrawal', 'Total population']
'''filter countries (no filter if empty)'''
filter_countries = []

data = df[['Country', 'Year', *relevant_vars]]
if filter_countries:
    data = data[data['Country'].isin(filter_countries)]
data = data.dropna()

years = df['Year'].unique()
years = years[years > target_year]

years_np_arr = np.zeros(years.shape[0])
water = np.zeros((years.shape[0], len(relevant_vars)))
population = np.zeros(years.shape[0])

for i, year in enumerate(years):
    # filter dataframe w.r.t. year 
    years_np_arr[i] = year
    df_filtered = data[data["Year"] == year]
    for j, var in enumerate(relevant_vars):
        if var != 'Total population':
            water[i,j] = df_filtered[var].sum()
        else:
            population[i] = df_filtered[var].sum()

fig, ax = plt.subplots()

ax.set_title('Global Freshwater Withdrawal', fontsize=10)

# Grid
ax.grid(True, which='major', color=rgb.tue_gray, alpha=0.5)

# X-axis
ax.set_xlabel('Year')
ax.xaxis.set_ticks_position('both')
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.set_ylabel("Freshwater Withdrawal ($10^9$ m3/year)")

width = 0.4
#ax.bar(years_np_arr - width / 2, water[:,0], width, color = rgb.tue_blue)
ax.bar(years_np_arr + width / 2, water[:,3], bottom = water[:,1] + water[:,2], width = width, color = rgb.tue_green, label = 'Agricultural Sector')
ax.bar(years_np_arr + width / 2, water[:,2], bottom = water[:,1], width = width, color = rgb.tue_gray, label = 'Industrial Sector')
ax.bar(years_np_arr + width / 2, water[:,1], width = width, color = rgb.tue_orange, label = 'Municipal Sector')

#plot population on second y axis
ax2 = ax.twinx()
ax2.plot(years_np_arr, population * 1000, color = rgb.tue_red, label = 'Population')
ax2.set_ylim(bottom = 0)
ax2.set_ylabel("Global Population")

# Add a legend
#ax.legend(relevant_vars, loc='upper left', frameon=False)

# Add source
ax.text(0.99, 0.01, 'Source: FAO AQUASTAT', transform=ax.transAxes, fontsize=8, ha='right', color=rgb.tue_gray)

# plot legends in one window
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc=0)

plt.show()
