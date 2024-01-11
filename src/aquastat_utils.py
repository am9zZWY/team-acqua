import os
from pathlib import Path

import pandas as pd

from src.utils import get_dataframe

PATH_TO_DAT = Path(__file__).parent / '..' / 'dat'
FILE_NAME = 'fao_aquastat.csv'
CSV_URL = 'https://yaon.org/data.csv'


def get_aquastat(raw=False) -> pd.DataFrame | None:
    file_path = os.path.join(PATH_TO_DAT, FILE_NAME)
    print(f'Getting AQUASTAT dataframe from {file_path} ...')

    # Download the data from https://yaon.org/data.csv
    import_df = get_dataframe(file_path=file_path, url=CSV_URL)
    if import_df is None:
        print('Could not get the AQUASTAT Dataframe!')
        return None

    # Format dataframe
    import_df.drop(columns=['Unnamed: 0'], inplace=True)

    # Return raw dataframe
    if raw:
        return import_df

    # Pivot table
    df = import_df.pivot_table(index=['Country', 'Year'], columns='Variable', values='Value', aggfunc='first')
    df.reset_index(inplace=True)

    return df
