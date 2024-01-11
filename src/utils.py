import math

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
import os.path

OUT_PATH = 'out'


def download_file(file_path=None, url=None) -> bool:
    """
    Downloads data from a url and saves it to a file.

    :param file_path: the location to save the file to
    :param url: the URL to download from
    :return: bool indicating success
    """

    if file_path is None or url is None:
        print('No file name or url specified!')
        return False

    if os.path.isfile(file_path):
        print(f'{file_path} already exists.')
    else:
        print(f'{file_path} does not exist.')
        print(f'Downloading {file_path} ...')
        r = requests.get(url)
        with open(file_path, 'wb') as f:
            bytes_written = f.write(r.content)
            if bytes_written == 0:
                print(f'Error downloading {file_path}!')
                return False

    # If we get here, the file exists
    return True


def get_dataframe(file_path=None, url=None) -> pd.DataFrame | None:
    """
    Downloads data from a url and saves it to a file.
    If the file does not exist, it will be downloaded from the url.

    Creates a pandas dataframe from the csv file and returns it

    :param file_path: the location where the file is opened from
    :param url: the URL to download from
    :return: pandas dataframe or None if the file could not be downloaded
    """

    if file_path is None or url is None:
        print('No file name or url specified!')
        return None

    if not download_file(file_path=file_path, url=url):
        print(f'Cannot create dataframe from {file_path}!')
        return None

    import_df = pd.read_csv(file_path)
    return import_df


def save_fig(fig, fig_name=None, out_path=None) -> bool:
    """
    Saves a figure to a file.

    :param fig: the figure to save
    :param fig_name: the name of the figure
    :param out_path: the location to save the figure to
    :return: bool indicating success
    """

    if fig_name is None or out_path is None:
        print('No figure_name or out path specified!')
        return False

    # If fig_name does not begin with 'fig_', add it
    if not fig_name.startswith('fig_'):
        fig_name = f'fig_{fig_name}'

    # If out_path does not exist, create it
    if not os.path.isdir(out_path):
        print(f'{out_path} does not exist.')
        print(f'Creating {out_path} ...')
        os.makedirs(out_path, exist_ok=True)

    print(f'Saving figure to {out_path} ...')
    fig.savefig(os.path.join(OUT_PATH, out_path, f'{fig_name}.pdf'), dpi=300, bbox_inches='tight')
    return True


def show_data(df, variables, include_countries=None):
    """
    Creates a plot showing whether data exists for variables in countries and years.
    If multiple variable names are given it looks if all are present for a year/country.

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
    blue_patch = mpatches.Patch(color=color_0, label='no data')
    red_patch = mpatches.Patch(color=color_1, label='data')
    plt.legend(handles=[blue_patch, red_patch], loc='upper left')

    plt.title('Presence of variables in year')
    plt.xlabel('year')
    plt.ylabel('country')

    plt.tight_layout()
    plt.show()


def quality_map(df, variables, include_countries=None):
    '''Plot a map to show the quality of the data for each country'''
    if include_countries is None:
        include_countries = []

    if isinstance(variables, str):
        variables = [variables]

    '''Extract relevant variables and drop all NaN'''
    data = df[['Country', 'Year', *variables]]
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
    rename_to_dict = {
        'Russian Federation': 'Russia',
        'Bolivia (Plurinational State of)': 'Bolivia'
        # TODO
    }
    for key, value in rename_to_dict.items():
        countries_df.rename(index={key: value}, inplace=True)

    '''Create map'''
    plt.figure(figsize=(10, math.ceil(math.log(years_data['Country'].nunique(), 2)) * 5))
    '''Plot using geopandas'''
    import geopandas as gpd

    world = gpd.read_file(os.path.relpath('../dat/naturalearth/ne_110m_admin_0_countries.shx'), engine="pyogrio")
    world = world.merge(countries_df, left_on='SOVEREIGNT', right_on='Country')
    world.plot(column='True_Count', cmap='RdYlGn', legend=True, figsize=(20, 20),
               legend_kwds={'label': "Data Quality", 'orientation': "horizontal", 'shrink': 0.5})

    plt.title('Presence of variables in year')

    '''Remove axis'''
    plt.axis('off')

    plt.show()
