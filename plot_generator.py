import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import AutoMinorLocator, LogLocator
from tueplots.constants.color import rgb

# ENTER YOUR VARIABLE HERE
# ========================
variable = 'Treated municipal wastewater'

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
relevant_vars = [variable,
                 ]
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

# Iterate over unique countries in the dataset
for country in df['Country'].unique():
    # Filter data for the current country
    country_data = df[df['Country'] == country]
    data = country_data['Year']

    # Stats
    max_value = country_data[variable].max()
    min_value = country_data[variable].min()
    range_value = max_value - min_value

    # Create a figure and an axes
    fig, ax = plt.subplots()

    # Plotting
    ax.plot(data, country_data[variable],
            marker='o', linestyle='-', color=rgb.tue_blue, linewidth=1, markersize=3)

    # X-axis
    ax.set_xlabel('year')
    ax.xaxis.set_ticks_position('both')
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

    # Y-axis
    ax.set_ylabel(var_unit_map[variable])
    ax.yaxis.set_ticks_position('both')

    # Title
    ax.set_title(f'{variable} in {country} over time')

    # Show the plot
    ax.grid(axis="both", which="both", color=rgb.tue_gray, linewidth=0.5)

    # Save the plot as an image in the 'x' folder
    output_filename = os.path.join(output_folder, f'{country}_plot.png')
    fig.savefig(output_filename)

    # Close the plot to avoid displaying it in the loop
    plt.close()

    print(f"Generating plot for {country}")

print("Plots saved!")
