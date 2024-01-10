import math

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
import os.path

CSV_URL = 'https://yaon.org/data.csv'
FILE_NAME = 'dat/fao_aquastat.csv'


def download_file(file_name=FILE_NAME, url=CSV_URL) -> bool:
    """
    Downloads the data from https://yaon.org/data.csv
    but can also be used to load the data from a local file or a different url

    :param file_name: the location to save the file to
    :param url: the URL to download from
    :return: bool indicating success
    """

    if os.path.isfile(file_name):
        print(f'{file_name} already exists.')
    else:
        print(f'{file_name} does not exist.')
        print(f'Downloading {file_name} ...')
        r = requests.get(url)
        with open(file_name, 'wb') as f:
            bytes_written = f.write(r.content)
            if bytes_written == 0:
                print(f'Error downloading {file_name}!')
                return False

    # If we get here, the file exists
    return True


def get_dataframe(file_name=FILE_NAME, url=CSV_URL) -> pd.DataFrame | None:
    """
    Downloads the data from https://yaon.org/data.csv
    but can also be used to load the data from a local file or a different url

    If the file does not exist, it will be downloaded from the url

    Creates a pandas dataframe from the csv file and returns it

    :param file_name: the location where the file is opened from
    :param url: the URL to download from
    :return: pandas dataframe or None if the file could not be downloaded
    """

    if not download_file(file_name=file_name, url=url):
        print(f'Cannot create dataframe from {file_name}!')
        return None

    import_df = pd.read_csv(file_name)
    return import_df


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