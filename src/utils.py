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
