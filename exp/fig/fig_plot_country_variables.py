import matplotlib.pyplot as plt
from tueplots.constants.color import rgb

from src.aquastat_utils import get_aquastat, AQUASTAT_SOURCE
from src.utils import save_fig

# ENTER YOUR VARIABLE HERE
# ========================
RELEVANT_VARS = ['% of the cultivated area equipped for irrigation', '% of total country area cultivated']

# Download the data from https://yaon.org/data.csv

FIG_PATH = 'fig_plot_country_variables'

df = get_aquastat()
raw_df = get_aquastat(raw=True)

'''Create a dictionary with the units of each variable'''
var_unit_map = raw_df[['Variable', 'Unit']].drop_duplicates().set_index('Variable').to_dict()['Unit']

'''relevant variables for us'''
# TODO: Fix this
# df['% of the total area equipped for irrigation'] = df['% of the cultivated area equipped for irrigation'] * df['% of total country area cultivated']

'''filter countries (no filter if empty)'''
filter_countries = []

'''Extract relevant variables and drop all NaN'''
df = df[['Country', 'Year', *RELEVANT_VARS]]
if filter_countries:
    df = df[df['Country'].isin(filter_countries)]
df = df.dropna()

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
    ax.set_title('{} in {} ({}-{})'.format(" and\n".join(RELEVANT_VARS), country, years_range[0], years_range[1]),
                 fontsize=10, pad=10,
                 color=rgb.tue_darkblue)

    # Grid
    ax.grid(True, which='both', color=rgb.tue_gray, linestyle='--', alpha=0.5)

    # X-axis
    ax.set_xlabel('year')
    ax.xaxis.set_ticks_position('both')
    ax.xaxis.set_minor_locator(plt.MultipleLocator(1))

    # Iterate through all variables
    for (index, variable) in enumerate(RELEVANT_VARS):
        if variable not in df.columns:
            continue

        # Filter data for the current variable
        data = country_data[variable]

        # Plotting
        # For each variable, use a different color
        color = colors[index % len(colors)]
        ax.plot(years, data, marker='o', linestyle='-', color=color, linewidth=1, markersize=3)

        # Y-axis
        ax.set_ylabel(var_unit_map[variable])
        ax.yaxis.set_ticks_position('both')

    # Add a legend
    ax.legend(RELEVANT_VARS, loc='upper left', frameon=False)

    # Add source
    ax.text(0.99, 0.01, AQUASTAT_SOURCE, transform=ax.transAxes, fontsize=8, ha='right', color=rgb.tue_gray)

    # Show the plot
    # Save the plot as an image in the 'x' folder
    save_fig(fig, fig_name=f'{country}_plot', fig_path=FIG_PATH)

    # Close the plot to avoid displaying it in the loop
    plt.close()

print("Plots saved!")

# %%
