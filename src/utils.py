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
