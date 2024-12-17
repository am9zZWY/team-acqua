import os
from pathlib import Path

import geopandas as gpd
import math
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tueplots import bundles
from tueplots.constants.color import rgb

from src.utils import get_dataframe, to_dat_path

plt.rcParams.update(bundles.icml2022())
plt.rcParams.update({"figure.dpi": 200})

PATH_TO_DAT = Path(__file__).parent / '..' / 'dat'
FILE_NAME = 'fao_aquastat.csv'
CSV_URL = 'https://yaon.org/data.csv'

AQUASTAT_COUNTRY_MAPPING = {
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Brunei Darussalam': 'Brunei',
    'Congo': 'Republic of the Congo',
    "Côte d'Ivoire": 'Ivory Coast',
    "Democratic People's Republic of Korea": 'North Korea',
    'Dominica': 'Dominica',
    'Eswatini': 'Eswatini',
    'Faroe Islands': 'Faroe Islands',
    'Grenada': 'Grenada',
    'Holy See': 'Vatican City',
    'Iran (Islamic Republic of)': 'Iran',
    'Kiribati': 'Kiribati',
    "Lao People's Democratic Republic": 'Laos',
    'Liechtenstein': 'Liechtenstein',
    'Maldives': 'Maldives',
    'Malta': 'Malta',
    'Marshall Islands': 'Marshall Islands',
    'Mauritius': 'Mauritius',
    'Micronesia (Federated States of)': 'Micronesia',
    'Monaco': 'Monaco',
    'Nauru': 'Nauru',
    'Netherlands (Kingdom of the)': 'Netherlands',
    'Niue': 'Niue',
    'Palau': 'Palau',
    'Palestine': 'State of Palestine',
    'Puerto Rico': 'Puerto Rico',
    'Republic of Korea': 'South Korea',
    'Republic of Moldova': 'Moldova',
    'Russian Federation': 'Russia',
    'Saint Kitts and Nevis': 'Saint Kitts and Nevis',
    'Saint Lucia': 'Saint Lucia',
    'Saint Vincent and the Grenadines': 'Saint Vincent and the Grenadines',
    'Samoa': 'Samoa',
    'San Marino': 'San Marino',
    'Sao Tome and Principe': 'Sao Tome and Principe',
    'Serbia': 'Serbia',
    'Seychelles': 'Seychelles',
    'Singapore': 'Singapore',
    'Syrian Arab Republic': 'Syria',
    'Timor-Leste': 'East Timor',
    'Tokelau': 'Tokelau',
    'Tonga': 'Tonga',
    'Tuvalu': 'Tuvalu',
    'Türkiye': 'Turkey',
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Viet Nam': 'Vietnam',
}

AQUASTAT_SOURCE = 'Source: AQUASTAT'


def get_aquastat(raw=False) -> pd.DataFrame | None:
    file_path = FILE_NAME
    print(f'Getting AQUASTAT dataframe from {file_path} ...')

    # Download the data from https://yaon.org/data.csv
    import_df = get_dataframe(file_path=file_path, url=CSV_URL)
    if import_df is None:
        print('Could not get the AQUASTAT Dataframe!')
        return None

    # Format dataframe
    import_df.drop(columns=['Unnamed: 0'], inplace=True)

    # Fix some variables
    map_dict = {
        'Area equipped for irrigation by direct use of non-treated municipal wastewater ': 'Area equipped for irrigation by direct use of not treated municipal wastewater'
    }
    for key, value in map_dict.items():
        import_df.replace(to_replace={key: value}, inplace=True)

    # Return raw dataframe
    if raw:
        return import_df

    # Pivot table
    df = import_df.pivot_table(index=['Country', 'Year'], columns='Variable', values='Value', aggfunc='first')
    df.reset_index(inplace=True)

    # Rename some countries to be compatible with the world map
    rename_aquastat_countries(df)

    return df


def rename_aquastat_country(country):
    global AQUASTAT_COUNTRY_MAPPING

    if country in AQUASTAT_COUNTRY_MAPPING:
        return AQUASTAT_COUNTRY_MAPPING[country]
    return country


def rename_aquastat_countries(df):
    global AQUASTAT_COUNTRY_MAPPING
    print('Renaming countries ...')

    for country in df['Country'].unique():
        if country in AQUASTAT_COUNTRY_MAPPING:
            df.replace(to_replace={country: AQUASTAT_COUNTRY_MAPPING[country]}, inplace=True)


VAR_TO_UNIT_DICT = get_aquastat(True)[['Variable', 'Unit']].drop_duplicates().set_index('Variable').to_dict()['Unit']
