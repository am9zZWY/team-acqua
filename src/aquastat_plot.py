import math

import geopandas as gpd
import matplotlib
import pandas as pd
from scipy.stats import linregress
import seaborn as sns
from matplotlib import patches, pyplot as plt
import matplotlib.ticker as mticker

from tueplots import bundles
from tueplots.constants.color import rgb

from src.aquastat_utils import rename_aquastat_country, AQUASTAT_SOURCE
from src.utils import make_list, save_fig, to_dat_path


def show_data(df, variables, include_countries=None):
    """
    Creates a plot showing whether data exists for variables in countries and years.
    If multiple variable names are given, it looks if all are present for a year/country.

    :param df: Dataframe.
    :param variables: Variables to check for.
    :param include_countries: Optional. Filter for specific countries.
    """
    if include_countries is None:
        include_countries = []

    if isinstance(variables, str):
        variables = [variables]

    '''Extract relevant variables and drop all NaN'''
    data = df[['Country', 'Year', *variables]]
    if include_countries:
        data = data[data['Country'].isin(include_countries)]
    data = data.dropna()

    '''Create dataframe for heatmap'''
    years_data = data[['Country', 'Year']]
    years_df = years_data.pivot_table(index=['Country'], columns='Year', values='Year', aggfunc=lambda x: True,
                                      fill_value=False)
    years_df['True_Count'] = years_df.sum(axis=1)
    years_df = years_df.sort_values(by='True_Count', ascending=True)
    years_df.drop('True_Count', axis=1, inplace=True)

    df_numeric = years_df.replace({True: 1, False: 0})

    '''spaß mit colormap'''
    cmap_name = 'RdYlGn'
    cmap = matplotlib.colormaps[cmap_name]
    color_0 = cmap(0.0)
    color_1 = cmap(1.0)

    '''create heatmap'''
    plt.figure(figsize=(10, math.ceil(math.log(years_data['Country'].nunique(), 2)) * 5))
    ax = sns.heatmap(df_numeric,
                     annot=False,
                     cmap=cmap_name,
                     linewidths=0.5,
                     linecolor='gray',
                     cbar=False,
                     vmin=0,
                     vmax=1
                     )

    # Manuelle Legende
    blue_patch = patches.Patch(color=color_0, label='no data')
    red_patch = patches.Patch(color=color_1, label='data')
    plt.legend(handles=[blue_patch, red_patch], loc='upper left')

    plt.title('Presence of variables in year')
    plt.xlabel('year')
    plt.ylabel('country')

    plt.tight_layout()
    plt.show()


def plot_quality(aquastat_dataframe, variables, include_countries=None):
    """
    Plot a map to show the quality of the data for each country
    :param aquastat_dataframe: Dataframe.
    :param variables: Variables to check for.
    :param include_countries: Optional. Filter for specific countries.
    """
    if include_countries is None:
        include_countries = []

    if isinstance(variables, str):
        variables = [variables]

    '''Extract relevant variables and drop all NaN'''
    data = aquastat_dataframe[['Country', 'Year', *variables]]
    if include_countries:
        data = data[data['Country'].isin(include_countries)]
    data = data.dropna()

    '''Create dataframe for map'''
    countries_data = data[['Country', 'Year']]
    countries_df = countries_data.pivot_table(index=['Country'], columns='Year', values='Year', aggfunc=lambda x: True,
                                              fill_value=False)
    countries_df['True_Count'] = countries_df.sum(axis=1) / countries_df.shape[1]
    countries_df = countries_df.sort_values(by='True_Count', ascending=True)

    years_data = data[['Country', 'Year']]
    years_df = years_data.pivot_table(index=['Country'], columns='Year', values='Year', aggfunc=lambda x: True,
                                      fill_value=False)
    years_df['True_Count'] = years_df.sum(axis=1)
    years_df = years_df.sort_values(by='True_Count', ascending=True)
    years_df.drop('True_Count', axis=1, inplace=True)

    '''Rename some countries'''
    for country in countries_df['Country'].unique():
        replace_to = rename_aquastat_country(country)
        countries_df.replace(to_replace={country: replace_to}, inplace=True)

    '''Create map'''
    plt.figure(figsize=(10, math.ceil(math.log(years_data['Country'].nunique(), 2)) * 5))
    '''Plot using geopandas'''

    world = gpd.read_file(to_dat_path('naturalearth/ne_110m_admin_0_countries.shx'), engine="pyogrio")
    world = world.merge(countries_df, left_on='SOVEREIGNT', right_on='Country')
    world.plot(column='True_Count', cmap='RdYlGn', legend=True, figsize=(20, 20),
               legend_kwds={'label': "Data Quality", 'orientation': "horizontal", 'shrink': 0.5})

    plt.title('Presence of variables in year')

    plt.axis('on')
    plt.grid(which='major', axis='both', linestyle='-', color='lightgrey', alpha=0.5)

    plt.show()


def plot_world(aquastat_dataframe, variables, year, title=None, include_countries=None, 
               cmap='RdYlGn', vmin = 0, vmax = 40, label = "Withdrawal (\%) of total renewable water resources"):
    """
    Plot a map to show the quality of the data for each country
    :param aquastat_dataframe: Dataframe.
    :param variables: Variables to check for.
    :param include_countries: Optional. Filter for specific countries.
    """
    if include_countries is None:
        include_countries = []

    if isinstance(variables, str):
        variables = [variables]

    if year is None:
        print('No year specified!')
        return None

    if title is None:
        title = 'World Map'

    # Extract relevant variables and drop all NaN
    data = aquastat_dataframe[['Country', 'Year', *variables]]
    data = data.dropna()

    # Filter for specific year
    countries_df = data[data['Year'] == year]

    # Aggregate data
    countries_df = countries_df[['Country', *variables]]

    # Rename countries to match the world map
    for country in countries_df['Country'].unique():
        replace_to = rename_aquastat_country(country)
        countries_df.replace(to_replace={country: replace_to}, inplace=True)

    # Merge data with world map
    world = gpd.read_file(to_dat_path(file_path='naturalearth/ne_110m_admin_0_countries.shx'), engine="pyogrio")
    world = world.merge(countries_df, left_on='SOVEREIGNT', right_on='Country')

    plt.rcParams.update(bundles.icml2022(column='half', nrows=1, ncols=1))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Create figure
    # plt.figure(figsize=(10, math.ceil(math.log(countries_df['Country'].nunique(), 2)) * 5))

    # Plot using geopandas
    world.plot(column=variables[0], ax=ax, vmin=vmin, vmax=vmax, legend=True, figsize=(20, 20), cmap=cmap,
               legend_kwds={'label': label, 'orientation': "horizontal",
                            'shrink': 0.5, 'extend': 'max'})

    ax.set_title(title)
    ax.axis("off")
    ax.grid(which='major', axis='both', linestyle='-', color='lightgrey', alpha=0.5)
    # Add source
    plt.text(0.5, 0.05, AQUASTAT_SOURCE, fontsize='xx-small', horizontalalignment='center', verticalalignment='center',
             transform=plt.gca().transAxes, color=rgb.tue_gray)

    return plt


def get_growth_rate(series, log_scale=False):
    """
    Calculate the relative growth rate of a series.
    !! It only looks at the first and last value in series !!
    :param series: series to calculate relative growth rate for.
    :return: Relative growth rate.
    """
    y = series.values
    rate = ((y[-1] - y[0]) / y[0]) * 100
    if rate == 0:
        return 0

    # If log scale is true, use log10
    if log_scale:
        # If rate is negative, use -log10(-rate)
        if rate > 0:
            rate = math.log10(rate)
        # ... else use log10(rate)
        else:
            rate = -math.log10(-rate)
    return rate

def get_slope(series, log_scale):
    y = series.values
    x = series.index

    slope = linregress(x, y).slope

    # If log scale is true, use log10
    if log_scale:
        # If rate is negative, use -log10(-rate)
        if slope > 0:
            slope = math.log10(slope)
        # ... else use log10(rate)
        elif slope == 0:
            slope = 0
        else:
            slope = -math.log10(abs(slope))

    return slope


def plot_growth_rate(
        data: pd.DataFrame,
        variables: str,
        cmaps: str = 'cividis',
        title_vars: str = None,
        log_scale: bool = False,
        fig=None,
        axs=None,
        slope=False
):
    """
    Plot relative growth rates for a variable on a world map. Can plot multiple
    maps next to each other.
    :param data: Dataframe containing countries, years, and variables to plot.
    :param variables: Variables to plot.
    :param cmaps: Preferred colormap for plotting. The default is 'cividis'.
                Multiple colormaps can be given.
    :param title_vars: Preferred form of variables in title.
    :param log_scale: Whether to use a log scale for the growth rates.
    :return: Fig, axs (matplotlib figure and axes objects)
    """
    '''constants'''
    font_size = 15
    world = gpd.read_file(to_dat_path(file_path='naturalearth/ne_110m_admin_0_countries.shx'), engine="pyogrio")

    # missing data colors:
    md_facecolor = "white"
    md_edgecolor = "grey"

    # slope or gr
    sc = ''
    if slope:
        method = get_slope

        label = f'Linear regression coefficient'
    else:
        method = get_growth_rate

        label = f'Relative Growth Rate [$\%$]'

    '''ready input for subplots'''
    variables = make_list(variables, 1)
    plots = len(variables)

    # Create fig and ax if not provided
    if not fig or not axs:
        fig, axs = plt.subplots(1, plots, figsize=(15 * plots, 10))

    if plots == 1:
        axs = [axs]
    cmaps = make_list(cmaps, plots)
    title_vars = make_list(title_vars, 1)
    if len(title_vars) != plots:
        title_vars = [None] * plots

    '''plot subplots'''
    for ax, variable, cmap, title_var in zip(axs, variables, cmaps, title_vars):
        '''Get Rates'''
        # Pivot the DataFrame to have years as the index and countries as columns
        df_pivot = data.pivot(index='Year', columns='Country', values=variable).dropna()
        # Apply the function to calculate growth rate for each country
        rates = df_pivot.apply(method, log_scale=log_scale)
        # Convert the results to a DataFrame
        rates_df = rates.reset_index(name='Relative growth rate')

        # Get map
        # Join Data to map
        merged = world.set_index('SOVEREIGNT').join(rates_df.set_index('Country'))
        vmax = max(abs(merged['Relative growth rate'].min()), merged['Relative growth rate'].min())

        # Plotting
        merged.plot(
            column='Relative growth rate',
            ax=ax, legend=True,
            missing_kwds={"color": md_facecolor, "edgecolor": md_edgecolor, "label": "No Data", "hatch": "//"},
            cmap=cmap,
            vmin=-vmax, vmax=vmax,
            edgecolor='black',  # Add black borders for each country
            linewidth=0.8,  # Adjust line width of the borders
            legend_kwds={
                'label': label,
                'orientation': "horizontal",
            }
        )

        # Set title
        years = df_pivot.index
        if not title_var:
            title_var = variable
        plottitle = f'Growth of {title_var} ({years.min()} - {years.max()})'
        if plots > 1:
            plottitle = title_var
        ax.set_title(plottitle, fontsize=font_size * (4 / 3))

        # Change font sizes
        cbar = fig.axes[-1]
        cbar.set_xlabel(label,
                        fontsize=font_size)

        if log_scale:
            cbar.xaxis.set_major_formatter(mticker.FuncFormatter(format_tick))

        for label in cbar.get_xticklabels():
            label.set_fontsize(font_size)

        # Create a custom legend patch for "No Data"
        no_data_patch = patches.Patch(facecolor=md_facecolor, edgecolor=md_edgecolor, label='No Data', hatch='//')
        ax.legend(handles=[no_data_patch], loc='upper right', fontsize=font_size)

        # Remove axis
        ax.axis('off')

        # Add source text
        fig.text(0.95, 0.01, AQUASTAT_SOURCE,
                 verticalalignment='bottom', horizontalalignment='right',
                 transform=ax.transAxes,
                 color='grey', fontsize=font_size * (2 / 3))

    # Add main title
    if plots > 1:
        fig.suptitle(f'Growth of Variables ({years.min()} - {years.max()})', fontsize=font_size * (5 / 3))

    # Save figure
    save_name = '_and_'.join(variables)
    save_fig(fig, f'growth_rate_{save_name.replace(" ", "_")}', 'water_management', experimental=True)

    return fig, axs

def format_tick(val, pos):
    """Konvertiert log10-Werte zurück zu ursprünglichen Werten."""
    return f"{10**val:.0f}"