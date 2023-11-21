import math

import pandas as pd
import matplotlib.pyplot as plt
import os
from tueplots.constants.color import rgb

# ENTER YOUR VARIABLE HERE
# ========================
variables = ['Total water withdrawal per capita', 'Total renewable water resources per capita']

# Download the data from https://yaon.org/data.csv


print("Loading Dataset")

'''import csv'''
csv_path = 'data.csv'
import_df = pd.read_csv(csv_path)
import_df.drop(columns=['Unnamed: 0'], inplace=True)
'''Format dataframe'''
df = import_df.pivot_table(index=['Country', 'Year'], columns=['Variable'], values='Value', aggfunc='first')
df.reset_index(inplace=True)

'''Create a dictionary with the units of each variable'''
var_unit_map = import_df[['Variable', 'Unit']].drop_duplicates().set_index('Variable').to_dict()['Unit']

'''relevant variables for us'''
relevant_vars = variables

'''filter countries (no filter if empty)'''
filter_countries = []

'''Extract relevant variables and drop all NaN'''
data = df[['Country', 'Year', *relevant_vars]]
if filter_countries:
    data = data[data['Country'].isin(filter_countries)]
data = data.dropna()

# Create the 'x' folder if it doesn't exist
output_folder = 'plots'
os.makedirs(output_folder, exist_ok=True)

colors = [rgb.tue_blue, rgb.tue_red, rgb.tue_green, rgb.tue_orange]

# Iterate over unique countries in the dataset
for country in df['Country'].unique():
    print(f"Generating plot for {country}")

    # Filter data for the current country
    country_data = df[df['Country'] == country]
    years = country_data['Year']
    years_range = [min(years), max(years)]

    # Create a figure and an axes
    fig, ax = plt.subplots()

    # Set the title
    ax.set_title('{} in {} ({}-{})'.format(" and\n".join(variables), country, years_range[0], years_range[1]),
                 fontsize=10, pad=10,
                 color=rgb.tue_darkblue)

    # Grid
    ax.grid(True, which='both', color=rgb.tue_gray, linestyle='--', alpha=0.5)

    # X-axis
    ax.set_xlabel('year')
    ax.xaxis.set_ticks_position('both')
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

    for (index, variable) in enumerate(relevant_vars):
        if variable not in df.columns:
            continue

        data = country_data[variable]

        # Plotting
        color = colors[index % len(colors)]
        ax.plot(years, data, marker='o', linestyle='-', color=color, linewidth=1, markersize=3)

        # Y-axis
        ax.set_ylabel(var_unit_map[variable])
        ax.yaxis.set_ticks_position('both')

    # Add a legend
    ax.legend(relevant_vars, loc='upper left', frameon=False)

    # Add source
    ax.text(0.99, 0.01, 'Source: FAO AQUASTAT', transform=ax.transAxes, fontsize=8, ha='right', color=rgb.tue_gray)

    # Show the plot
    # Save the plot as an image in the 'x' folder
    output_filename = os.path.join(output_folder, f'{country}_plot.png')
    fig.savefig(output_filename)

    # Close the plot to avoid displaying it in the loop
    plt.close()

print("Plots saved!")
